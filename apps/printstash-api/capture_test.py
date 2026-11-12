import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from unittest.mock import patch

from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

from app.core.time import utcnow
from app.db.models import (
    CaptureUploadSlot,
    CaptureUploadSlotState,
    InboxItem,
    InboxItemState,
    InboxSourceKind,
    User,
)
from app.modules.ingestion import inbox, staging_leases


class QuarantineTests(unittest.TestCase):
    def test_owner_only_directories_allow_inherited_setgid(self):
        for mode in (0o700, 0o2700):
            with self.subTest(mode=oct(mode)), tempfile.TemporaryDirectory() as root:
                parent = Path(root) / "staging"
                parent.mkdir()
                parent.chmod(mode)
                source = parent / "owned"
                source.write_bytes(b"owned staging bytes")
                info = source.stat()

                self.assertTrue(
                    staging_leases._quarantine_owned_file(
                        source,
                        receipt_id="owned-receipt",
                        device=info.st_dev,
                        inode=info.st_ino,
                        ctime_ns=info.st_ctime_ns,
                        size_bytes=info.st_size,
                    )
                )
                self.assertFalse(source.exists())

    def test_unsafe_quarantine_modes_leave_owned_bytes_untouched(self):
        for mode in (0o750, 0o770, 0o1700, 0o4700):
            with self.subTest(mode=oct(mode)), tempfile.TemporaryDirectory() as root:
                source = Path(root) / "owned"
                source.write_bytes(b"preserve these bytes")
                info = source.stat()
                quarantine = Path(root) / ".printstash-staging-quarantine"
                quarantine.mkdir()
                quarantine.chmod(mode)

                self.assertFalse(
                    staging_leases._quarantine_owned_file(
                        source,
                        receipt_id="owned-receipt",
                        device=info.st_dev,
                        inode=info.st_ino,
                    )
                )
                self.assertEqual(source.read_bytes(), b"preserve these bytes")


class ResolverTests(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine(
            "sqlite://",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        self.addCleanup(self.engine.dispose)
        SQLModel.metadata.create_all(self.engine)
        with Session(self.engine) as session:
            owner = User(username="isolated-test-owner", hashed_password="!test-only")
            session.add(owner)
            session.flush()
            self.url_id = self.add_item(session, owner.id, InboxSourceKind.URL)
            self.legacy_id = self.add_item(session, owner.id, InboxSourceKind.BROWSER)
            self.capture_ids = []
            for state in (
                CaptureUploadSlotState.PENDING,
                CaptureUploadSlotState.UPLOADED,
            ):
                item_id = self.add_item(session, owner.id, InboxSourceKind.BROWSER)
                self.capture_ids.append(item_id)
                session.add(
                    CaptureUploadSlot(
                        id=f"test-slot-{item_id}",
                        inbox_item_id=item_id,
                        role="file",
                        source_file_id="test-file",
                        filename="test.stl",
                        media_type="model/stl",
                        size_bytes=4,
                        sha256="0" * 64,
                        state=state,
                        storage_key=f"test-slot/{item_id}",
                    )
                )
            session.commit()

    @staticmethod
    def add_item(session, owner_id, source_kind):
        item = InboxItem(
            owner_user_id=owner_id,
            source_kind=source_kind,
            state=InboxItemState.CAPTURED,
            source_url="https://example.com/model.stl",
        )
        session.add(item)
        session.flush()
        return item.id

    @contextmanager
    def scoped_session(self):
        with Session(self.engine) as session:
            yield session

    def test_pending_source_preserves_url_and_legacy_capture_resolution(self):
        with Session(self.engine) as session:
            pending = inbox.ResolveSource().pending(
                session, now=utcnow(), limit=20
            )
        self.assertEqual(
            {item.subject_key for item in pending},
            {f"inbox_item/{self.url_id}", f"inbox_item/{self.legacy_id}"},
        )

    def test_stale_resolver_cannot_claim_unfinalized_slot_captures(self):
        with patch.object(inbox, "get_session_factory", return_value=self):
            for item_id in self.capture_ids:
                with self.subTest(item_id=item_id):
                    self.assertEqual(
                        inbox._begin_resolve(item_id), (False, None, None)
                    )
                    with Session(self.engine) as session:
                        self.assertEqual(
                            session.get(InboxItem, item_id).state,
                            InboxItemState.CAPTURED,
                        )

    def test_ordinary_url_resolver_still_claims_its_work(self):
        with patch.object(inbox, "get_session_factory", return_value=self):
            started, source_url, owner_id = inbox._begin_resolve(self.url_id)
        self.assertTrue(started)
        self.assertEqual(source_url, "https://example.com/model.stl")
        self.assertIsNotNone(owner_id)


if __name__ == "__main__":
    unittest.main(verbosity=2)
