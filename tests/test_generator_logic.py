import unittest

from generator_logic import is_valid_device_name, parse_input_line


class ParseInputLineTests(unittest.TestCase):
    def test_parses_whitespace_delimited_input(self):
        self.assertEqual(parse_input_line("account01 device01"), ("account01", "device01"))

    def test_parses_csv_input(self):
        self.assertEqual(parse_input_line("account01, device01"), ("account01", "device01"))

    def test_parses_quoted_csv_fields(self):
        self.assertEqual(parse_input_line('"account, west",device01'), ("account, west", "device01"))

    def test_ignores_blank_lines_and_header(self):
        self.assertIsNone(parse_input_line("  "))
        self.assertIsNone(parse_input_line("account,device"))

    def test_rejects_malformed_rows(self):
        for line in ("account01", "account01,", '"account01,device01'):
            with self.subTest(line=line):
                with self.assertRaises(ValueError):
                    parse_input_line(line)


class DeviceNameTests(unittest.TestCase):
    def test_accepts_normal_device_names(self):
        self.assertTrue(is_valid_device_name("device-01"))

    def test_rejects_path_and_windows_filename_characters(self):
        for device in ("../device", "folder\\device", "bad:name", "device."):
            with self.subTest(device=device):
                self.assertFalse(is_valid_device_name(device))

    def test_rejects_reserved_windows_names(self):
        self.assertFalse(is_valid_device_name("CON"))
        self.assertFalse(is_valid_device_name("COM1.json"))


if __name__ == "__main__":
    unittest.main()