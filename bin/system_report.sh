#!/usr/bin/env bash
#
# System Diagnostic & Health Report Utility
# Generates concise Linux OS, load, memory, disk, and networking summaries.
#

set -euo pipefail

VERSION="1.0.0"

show_help() {
    cat << 'EOF'
Usage: system_report.sh [OPTIONS]

Generates a formatted Linux system diagnostic report.

Options:
  -h, --help       Show this help message and exit
  -v, --version    Show version information and exit
  -s, --short      Display only load, memory, and disk summaries
EOF
}

show_version() {
    echo "system_report.sh v${VERSION}"
}

SHORT_MODE=0

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -v|--version)
            show_version
            exit 0
            ;;
        -s|--short)
            SHORT_MODE=1
            shift
            ;;
        *)
            echo "Error: Unknown argument '$1'" >&2
            show_help >&2
            exit 1
            ;;
    esac
done

echo "================================================================================"
echo " SYSTEM HEALTH & DIAGNOSTIC REPORT ($(date -u '+%Y-%m-%d %H:%M:%S UTC'))"
echo "================================================================================"

echo ""
echo "--- [1] OS & KERNEL ---"
echo "Hostname:   $(hostname)"
echo "Kernel:     $(uname -r)"
if [ -f /etc/os-release ]; then
    # shellcheck disable=SC1091
    source /etc/os-release
    echo "OS:         ${PRETTY_NAME:-Linux}"
fi
echo "Uptime:    $(uptime -p 2>/dev/null || uptime)"

echo ""
echo "--- [2] CPU & LOAD AVERAGE ---"
echo "Load Avg:   $(awk '{print $1", "$2", "$3}' /proc/loadavg)"
echo "CPU Cores:  $(nproc)"

echo ""
echo "--- [3] MEMORY USAGE (MB) ---"
free -m

echo ""
echo "--- [4] DISK USAGE ---"
df -h -x tmpfs -x devtmpfs -x squashfs 2>/dev/null || df -h

if [ "$SHORT_MODE" -eq 0 ]; then
    echo ""
    echo "--- [5] TOP 5 PROCESSES BY MEMORY ---"
    ps aux --sort=-%mem | head -n 6 2>/dev/null || true

    echo ""
    echo "--- [6] LISTENING TCP PORTS ---"
    if command -v ss >/dev/null 2>&1; then
        ss -tulpn | grep LISTEN || true
    elif command -v netstat >/dev/null 2>&1; then
        netstat -tulpn | grep LISTEN || true
    else
        echo "Note: neither 'ss' nor 'netstat' is installed."
    fi
fi

echo ""
echo "================================================================================"
echo " END OF REPORT"
echo "================================================================================"
