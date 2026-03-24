"""File entrypoint used with `isaaclab -p` for Lab 01 foundations."""

from __future__ import annotations

import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lab_01_foundations.src.foundations_standalone import main


if __name__ == "__main__":
    raise SystemExit(main())
