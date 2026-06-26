#!/bin/bash
set -e
cd "$(dirname "${BASH_SOURCE[0]}")"

# Locate Qt6 rcc (pyrcc6 does not exist; Qt6 rcc --generator python replaces pyrcc5)
RCC=$(
    for candidate in \
        /usr/lib/qt6/libexec/rcc \
        /usr/lib/x86_64-linux-gnu/qt6/libexec/rcc \
        /usr/local/lib/qt6/libexec/rcc \
        rcc6 \
        qt6-rcc; do
        if command -v "$candidate" >/dev/null 2>&1 || [ -x "$candidate" ]; then
            echo "$candidate"
            break
        fi
    done
)

if [ -z "$RCC" ]; then
    echo "Error: Qt6 rcc not found. Install qt6-tools (e.g. apt install qt6-base-dev-tools)." >&2
    exit 1
fi

"$RCC" --generator python -o ../pysdb3_rc.py pysdb3.qrc
sed -i 's/from PySide6 import QtCore/from PyQt6 import QtCore/' ../pysdb3_rc.py
