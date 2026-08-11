#!/usr/bin/env python3
"""Build the native macOS LocalShare executable from the project root."""

from pathlib import Path
import platform
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
BUILD_VENV = PROJECT_ROOT / ".build-venv"
OUTPUT = PROJECT_ROOT / "dist" / "LocalShare"


def run(*command: str) -> None:
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def main() -> None:
    if platform.system() != "Darwin":
        raise SystemExit(
            "This builder must run on macOS. "
            "Use build_windows.bat on Windows or build_linux.sh on Linux."
        )

    print(f"Building LocalShare for macOS from:\n{PROJECT_ROOT}\n")

    print("[1/4] Preparing an isolated build environment...")
    build_python = BUILD_VENV / "bin" / "python"
    if not build_python.is_file():
        run(sys.executable, "-m", "venv", str(BUILD_VENV))

    print("[2/4] Installing build requirements...")
    run(str(build_python), "-m", "pip", "install", "-r", "requirements.txt")

    print("[3/4] Collecting Django static files...")
    run(str(build_python), "manage.py", "collectstatic", "--noinput")

    print("[4/4] Creating the macOS executable...")
    if OUTPUT.exists():
        OUTPUT.unlink()
    run(str(build_python), "-m", "PyInstaller", "--noconfirm", "--clean", "run.spec")

    if not OUTPUT.is_file():
        raise RuntimeError("PyInstaller finished but dist/LocalShare was not created.")

    print("\nBuild complete: dist/LocalShare")


if __name__ == "__main__":
    main()
