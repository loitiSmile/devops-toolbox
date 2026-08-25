import unittest
from unittest.mock import MagicMock, patch
from bin.ssl_checker import parse_args, get_certificate_info


class TestSSLChecker(unittest.TestCase):

    def test_parse_args_defaults(self):
        args = parse_args(["example.com"])
        self.assertEqual(args.host, "example.com")
        self.assertEqual(args.port, 443)
        self.assertEqual(args.warning_days, 14)
        self.assertEqual(args.timeout, 5.0)
        self.assertFalse(args.json)

    def test_parse_args_custom(self):
        args = parse_args(["myhost.net", "-p", "8443", "-w", "30", "--json", "-t", "10.0"])
        self.assertEqual(args.host, "myhost.net")
        self.assertEqual(args.port, 8443)
        self.assertEqual(args.warning_days, 30)
        self.assertEqual(args.timeout, 10.0)
        self.assertTrue(args.json)

    @patch("ssl.create_default_context")
    @patch("socket.socket")
    def test_get_certificate_info_valid(self, mock_socket, mock_ssl_context):
        mock_conn = MagicMock()
        mock_ctx_instance = MagicMock()
        mock_ssl_context.return_value = mock_ctx_instance
        mock_ctx_instance.wrap_socket.return_value = mock_conn

        mock_conn.getpeercert.return_value = {
            "notBefore": "Jan  1 00:00:00 2026 GMT",
            "notAfter": "Dec 31 23:59:59 2026 GMT",
            "subjectAltName": (("DNS", "example.com"), ("DNS", "www.example.com")),
            "issuer": ((("organizationName", "Let's Encrypt"),),),
        }

        data = get_certificate_info("example.com", port=443, timeout=5.0)

        self.assertEqual(data["hostname"], "example.com")
        self.assertEqual(data["port"], 443)
        self.assertEqual(data["issuer"], "Let's Encrypt")
        self.assertIn("example.com", data["sans"])
        self.assertIn("www.example.com", data["sans"])
        self.assertIsInstance(data["days_left"], int)


if __name__ == "__main__":
    unittest.main()
