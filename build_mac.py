#!/usr/bin/env python3
"""Build the native macOS LocalShare executable from the project root."""

from pathlib import Path
import platform
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
BUILD_VENV = PROJECT_ROOT / ".build-venv"
OUTPUTS = (
    PROJECT_ROOT / "dist" / "LocalShare.app",
    PROJECT_ROOT / "dist" / "LocalShare",
)


def run(*command: str) -> None:
    subprocess.run(command, cwd=PROJECT_ROOT, check=True)


def remove_previous_outputs() -> None:
    for output in OUTPUTS:
        if output.is_dir():
            shutil.rmtree(output)
        elif output.exists():
            output.unlink()


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
    remove_previous_outputs()
    run(str(build_python), "-m", "PyInstaller", "--noconfirm", "--clean", "run.spec")

    for output in OUTPUTS:
        if output.is_dir() or output.is_file():
            print(f"\nBuild complete: dist/{output.name}")
            return

    raise RuntimeError("PyInstaller finished but no LocalShare macOS application was created.")


if __name__ == "__main__":
    main()
