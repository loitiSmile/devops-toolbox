# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-08-25

### Added
- First-class support for `uv` package and environment manager.
- Package build system configuration via `pyproject.toml` and `hatchling`.
- CLI script entry point `ssl-checker` (`uv run ssl-checker`).
- CI pipeline acceleration using `astral-sh/setup-uv@v5`.
- Updated documentation with `uv` quickstart and command examples.

## [1.0.0] - 2026-08-25

### Added
- Initial release of `devops-toolbox`.
- `bin/ssl_checker.py`: CLI tool for inspecting remote SSL/TLS certificate health, expiration dates, SANs, and JSON output formatting.
- `bin/system_report.sh`: POSIX-compliant, ShellCheck-clean diagnostic tool generating concise CPU, load, memory, disk, and port summaries.
- Comprehensive unit tests for both Python and Shell utilities.
- Multi-version Python testing matrix (Python 3.10, 3.11, 3.12).
- Free automated CI & Security pipeline including ShellCheck, Ruff/Flake8, GitHub CodeQL SAST, and Gitleaks secret scanning.
