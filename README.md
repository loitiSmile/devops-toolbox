# devops-toolbox

[![CI & Security Pipeline](https://github.com/loitiSmile/devops-toolbox/actions/workflows/ci.yml/badge.svg)](https://github.com/loitiSmile/devops-toolbox/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Essential, tested, and secure DevOps CLI utilities for Linux system administration, network diagnostics, and SSL monitoring.

---

## ⚡ Quickstart with `uv`

This project is built and optimized for [`uv`](https://docs.astral.sh/uv/), the blazing-fast Python package manager:

```bash
# Run the SSL Checker directly with uv without manual environment setup
uv run ssl-checker github.com

# Run in JSON mode
uv run ssl-checker internal.corp.net -p 8443 --json

# Run all test suites
uv run python -m unittest discover -s tests/ -p "test_*.py"

# Run linters
uv run --extra dev ruff check bin/ tests/
```

---

## 🛠️ Included Tools

### 1. SSL Certificate Checker (`ssl-checker` / `bin/ssl_checker.py`)

Inspects remote TLS/SSL certificates, calculating exact days until expiration, issuer organization, and Subject Alternative Names (SAN). Supports structured JSON output for automated alerting.

```bash
# Using entry point via uv
uv run ssl-checker github.com

# Using direct script path
./bin/ssl_checker.py github.com -p 443 --warning-days 30
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

```bash
# Run Python Unit Tests with uv
uv run python -m unittest discover -s tests/ -p "test_*.py"

# Run Shell Script Tests
bash tests/test_system_report.sh
```

---

## 🔒 Security & CI Pipeline

This project adheres to strict automated quality and security checks via GitHub Actions:
- **Fast CI with uv:** Managed via `astral-sh/setup-uv@v5`.
- **Linting:** ShellCheck for shell scripts, Ruff & Flake8 for Python.
- **Unit Testing Matrix:** Tested against Python 3.10, 3.11, and 3.12.
- **SAST (Static Application Security Testing):** GitHub CodeQL security analysis.
- **Secret Detection:** Gitleaks scanning on all commits.

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) for details.

## 👤 Author

- **loiti**
