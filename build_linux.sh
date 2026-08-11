#!/usr/bin/env bash
# Build the native Linux LocalShare executable from the project root.
set -euo pipefail

PROJECT_ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
BUILD_VENV="${BUILD_VENV:-$PROJECT_ROOT/.build-venv}"
OUTPUT="$PROJECT_ROOT/dist/LocalShare"

cd "$PROJECT_ROOT"

if [[ "$(uname -s)" != "Linux" ]]; then
    echo "ERROR: This builder must run on Linux. Use build_windows.bat on Windows or build_mac.py on macOS." >&2
    exit 1
fi

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "ERROR: Python executable '$PYTHON_BIN' was not found." >&2
    exit 1
fi

echo "========================================"
echo "Building LocalShare for Linux from:"
echo "$PROJECT_ROOT"
echo "========================================"
echo

echo "[1/4] Preparing an isolated build environment..."
if [[ ! -x "$BUILD_VENV/bin/python" ]]; then
    "$PYTHON_BIN" -m venv "$BUILD_VENV"
fi
BUILD_PYTHON="$BUILD_VENV/bin/python"

echo "[2/4] Installing build requirements..."
"$BUILD_PYTHON" -m pip install -r requirements.txt

echo
echo "[3/4] Collecting Django static files..."
"$BUILD_PYTHON" manage.py collectstatic --noinput

echo
echo "[4/4] Creating the Linux executable..."
rm -f -- "$OUTPUT"
"$BUILD_PYTHON" -m PyInstaller --noconfirm --clean run.spec

if [[ ! -f "$OUTPUT" ]]; then
    echo "ERROR: PyInstaller finished but dist/LocalShare was not created." >&2
    exit 1
fi

echo
echo "========================================"
echo "Build complete: dist/LocalShare"
echo "========================================"
