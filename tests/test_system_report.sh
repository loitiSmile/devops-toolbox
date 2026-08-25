#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARGET_SCRIPT="${SCRIPT_DIR}/bin/system_report.sh"

echo "Running tests for system_report.sh..."

# Test 1: Help flag
"${TARGET_SCRIPT}" --help >/dev/null
echo "✓ Test --help passed"

# Test 2: Version flag
output=$("${TARGET_SCRIPT}" --version)
if [[ "${output}" =~ "system_report.sh v" ]]; then
    echo "✓ Test --version passed"
else
    echo "✗ Test --version failed: ${output}"
    exit 1
fi

# Test 3: Short mode execution
"${TARGET_SCRIPT}" --short >/dev/null
echo "✓ Test --short execution passed"

echo "All bash tests passed successfully."
