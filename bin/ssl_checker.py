#!/usr/bin/env python3
"""
SSL/TLS Certificate Expiration & Health Checker.

Retrieves and inspects remote SSL/TLS certificates, reporting days remaining
until expiration, issuer details, subject alternative names (SAN), and validity status.
"""

import argparse
import json
import socket
import ssl
import sys
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def get_certificate_info(hostname: str, port: int = 443, timeout: float = 5.0) -> Dict[str, Any]:
    """
    Connects to a remote host and fetches its TLS certificate.

    :param hostname: Target hostname (e.g. example.com)
    :param port: Target port (default: 443)
    :param timeout: Connection timeout in seconds
    :return: Dictionary containing certificate details
    """
    context = ssl.create_default_context()
    conn = context.wrap_socket(socket.socket(socket.AF_INET), server_hostname=hostname)
    conn.settimeout(timeout)

    try:
        conn.connect((hostname, port))
        cert: Any = conn.getpeercert()
    finally:
        conn.close()

    if not cert:
        raise ValueError(f"No certificate found on {hostname}:{port}")

    # Parse expiration date
    not_after_str = str(cert.get("notAfter", ""))
    not_before_str = str(cert.get("notBefore", ""))

    not_after = datetime.strptime(not_after_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)
    not_before = datetime.strptime(not_before_str, "%b %d %H:%M:%S %Y %Z").replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    days_left = (not_after - now).days
    is_expired = now > not_after

    # Extract Subject Alternative Names
    sans: List[str] = []
    alt_names = cert.get("subjectAltName") or ()
    for field in alt_names:
        if isinstance(field, tuple) and len(field) >= 2 and field[0] == "DNS":
            sans.append(str(field[1]))

    # Extract Issuer Common Name or Organization
    issuer_tuples = cert.get("issuer") or ()
    issuer_dict: Dict[str, str] = {}
    for item in issuer_tuples:
        if isinstance(item, tuple):
            for sub in item:
                if isinstance(sub, tuple) and len(sub) >= 2:
                    issuer_dict[str(sub[0])] = str(sub[1])

    issuer_name = issuer_dict.get("organizationName") or issuer_dict.get("commonName") or "Unknown"

    return {
        "hostname": hostname,
        "port": port,
        "valid_from": not_before.isoformat(),
        "valid_until": not_after.isoformat(),
        "days_left": days_left,
        "is_expired": is_expired,
        "issuer": issuer_name,
        "sans": sans,
    }


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Inspect SSL/TLS certificate expiration date, issuer, and health status."
    )
    parser.add_argument("host", help="Target hostname to check (e.g. github.com)")
    parser.add_argument("-p", "--port", type=int, default=443, help="Port number (default: 443)")
    parser.add_argument("-w", "--warning-days", type=int, default=14, help="Warning threshold in days (default: 14)")
    parser.add_argument("--json", action="store_true", help="Output results formatted as JSON")
    parser.add_argument("-t", "--timeout", type=float, default=5.0, help="Connection timeout in seconds (default: 5.0)")
    return parser.parse_args(args)


def main() -> int:
    args = parse_args()
    try:
        data = get_certificate_info(args.host, port=args.port, timeout=args.timeout)
    except Exception as exc:
        if args.json:
            print(json.dumps({"error": str(exc), "hostname": args.host}))
        else:
            print(f"Error checking {args.host}:{args.port} -> {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        status = "EXPIRED" if data["is_expired"] else "WARNING" if data["days_left"] <= args.warning_days else "OK"
        print(f"[{status}] {data['hostname']}:{data['port']}")
        print(f"  Issuer:       {data['issuer']}")
        print(f"  Valid Until:  {data['valid_until']} ({data['days_left']} days remaining)")
        print(f"  SANs:         {', '.join(data['sans'][:5])}{' ...' if len(data['sans']) > 5 else ''}")

    if data["is_expired"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
