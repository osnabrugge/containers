# PrintStash API capture fixes

This image extends the exact upstream v0.15.1 API image. It preserves the
upstream runtime and applies two narrow capture fixes:

- Permit an inherited setgid bit on an otherwise owner-only quarantine
  directory. Kubernetes `fsGroup` creates mode `2700`; access must still be
  `0700`. Inode, marker, lock, symlink and atomic-quarantine checks remain intact.
- Keep slot-backed browser captures out of URL resolution until explicit
  finalization, including stale queued resolver jobs.

The browser extension's separate upload deadline is not changed by this image.
There is no database migration or storage-provider change.

Run the app's normal container tests with `TEST_IMAGE` pointing to the built
image. They exercise real staging cleanup and isolated native SQLite resolver
queries, without production data or additional runtime test dependencies.

The upstream application is AGPL-3.0. Its source is
[xiao-villamor/PrintStash v0.15.1](https://github.com/xiao-villamor/PrintStash/tree/v0.15.1);
the complete downstream changes are in `capture.patch` beside this recipe.
