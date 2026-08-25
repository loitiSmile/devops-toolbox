# devops-toolbox

[![CI & Security Pipeline](https://github.com/loitiSmile/devops-toolbox/actions/workflows/ci.yml/badge.svg)](https://github.com/loitiSmile/devops-toolbox/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Essential, tested, and secure DevOps CLI utilities for Linux system administration, network diagnostics, and SSL monitoring.

---

## 🛠️ Included Tools

### 1. SSL Certificate Checker (`bin/ssl_checker.py`)

Inspects remote TLS/SSL certificates, calculating exact days until expiration, issuer organization, and Subject Alternative Names (SAN). Supports structured JSON output for automated alerting.

```bash
# Basic inspection
./bin/ssl_checker.py github.com

# Custom port with JSON output
./bin/ssl_checker.py internal.corp.net -p 8443 --json

# Set custom expiration warning threshold (days)
./bin/ssl_checker.py example.org -w 30
```

---

### 2. System Diagnostic & Health Report (`bin/system_report.sh`)

Generates a formatted, ShellCheck-compliant diagnostic overview of the host:
- Operating system and kernel release
- CPU cores and load averages
- Memory and swap consumption
- Disk usage per filesystem
- Top memory-consuming processes
- Active listening TCP ports

```bash
# Full report
./bin/system_report.sh

# Short summary mode (load, memory, disk only)
./bin/system_report.sh --short

# Help & Usage
./bin/system_report.sh --help
```

---

## 🧪 Testing & Code Quality

Run the local test suites:

```bash
# Run Python Unit Tests
python3 -m unittest discover -s tests/ -p "test_*.py"

# Run Shell Script Tests
bash tests/test_system_report.sh
```

---

## 🔒 Security & CI Pipeline

This project adheres to strict automated quality and security checks via GitHub Actions:
- **Linting:** ShellCheck for shell scripts, Ruff & Flake8 for Python.
- **Unit Testing Matrix:** Tested against Python 3.10, 3.11, and 3.12.
- **SAST (Static Application Security Testing):** GitHub CodeQL security analysis.
- **Secret Detection:** Gitleaks scanning on all commits.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.

## 👤 Author

- **loiti**
