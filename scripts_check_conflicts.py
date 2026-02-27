#!/usr/bin/env python3
"""Falla si existen marcadores de conflicto de git en archivos del repositorio."""

from pathlib import Path
import subprocess
import sys

START = "<<<<<<< "
MID = "======="
END = ">>>>>>> "


def tracked_files() -> list[Path]:
    out = subprocess.check_output(["git", "ls-files"], text=True)
    return [Path(p) for p in out.splitlines() if p]


def is_probably_text(path: Path) -> bool:
    binary_ext = {".png", ".jpg", ".jpeg", ".gif", ".pdf", ".zip", ".gz", ".so", ".db"}
    return path.suffix.lower() not in binary_ext


def main() -> int:
    hits: list[tuple[str, int, str]] = []

    for file_path in tracked_files():
        if not file_path.exists() or file_path.is_dir() or not is_probably_text(file_path):
            continue
        if str(file_path).startswith("venv/"):
            continue

        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            continue

        for line_no, line in enumerate(lines, start=1):
            if line.startswith(START) or line.startswith(END):
                hits.append((str(file_path), line_no, line.strip()))

    if hits:
        print("Se encontraron marcadores de conflicto sin resolver:")
        for path, line_no, line in hits:
            print(f" - {path}:{line_no}: {line}")
        print("\nResuelve los conflictos y vuelve a intentar.")
        return 1

    print("OK: no se encontraron marcadores de conflicto.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
