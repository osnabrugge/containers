import errno
import json
import subprocess
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, mock_open, patch

from smfc.hdfc import HdFc
from smfc.log import Log


class SensorFallbackTests(unittest.TestCase):
    def setUp(self):
        self.controller = HdFc.__new__(HdFc)
        self.controller.config = SimpleNamespace(smartctl_path="smartctl")
        self.controller.sudo = False
        self.controller.hd_device_names = ["/synthetic/disk"]
        self.controller.hwmon_path = ["/synthetic/hwmon"]
        self.controller.log = Mock()
        self.controller.log.log_level = Log.LOG_INFO

    def test_valid_hwmon_does_not_run_smartctl(self):
        with patch("builtins.open", mock_open(read_data="45000")), patch("subprocess.run") as run:
            self.assertEqual(self.controller._get_nth_temp(0), 45)
            run.assert_not_called()

    def test_fresh_valid_and_hot_values_are_preserved(self):
        for temperature, status in [(33, 0), (70, 0), (33, 8)]:
            with self.subTest(temperature=temperature, status=status):
                result = subprocess.CompletedProcess(
                    [], status, stdout=json.dumps({"temperature": {"current": temperature}}), stderr=""
                )
                with patch("builtins.open", side_effect=OSError(errno.EIO, "I/O error")), patch(
                    "subprocess.run", return_value=result
                ) as run:
                    self.assertEqual(self.controller._get_nth_temp(0), temperature)
                    run.assert_called_once_with(
                        ["smartctl", "-A", "-j", "/synthetic/disk"],
                        check=False, capture_output=True, text=True, timeout=5,
                    )
                self.assertEqual(self.controller.hwmon_path, ["/synthetic/hwmon"])
        self.assertEqual(self.controller.log.msg.call_count, 3)

    def test_unavailable_or_invalid_alternatives_remain_failures(self):
        cases = [
            ("{}", 0),
            ("not-json", 0),
            ('{"temperature":{"current":true}}', 0),
            ('{"temperature":{"current":0}}', 0),
            ('{"temperature":{"current":NaN}}', 0),
            ('{"temperature":{"current":45}}', 2),
        ]
        for output, status in cases:
            with self.subTest(output=output, status=status):
                result = subprocess.CompletedProcess([], status, stdout=output, stderr="")
                with patch("builtins.open", side_effect=OSError(errno.EIO, "I/O error")), patch(
                    "subprocess.run", return_value=result
                ), self.assertRaises(OSError):
                    self.controller._get_nth_temp(0)
        self.controller.log.msg.assert_not_called()

    def test_fallback_timeout_is_not_a_valid_temperature(self):
        with patch("builtins.open", side_effect=OSError(errno.EIO, "I/O error")), patch(
            "subprocess.run", side_effect=subprocess.TimeoutExpired("smartctl", 5)
        ), self.assertRaises(OSError):
            self.controller._get_nth_temp(0)


if __name__ == "__main__":
    unittest.main()
