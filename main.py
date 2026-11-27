"""Allow running from a source checkout with ``python main.py``."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))
from sentinel.app import main

if __name__ == "__main__":
    raise SystemExit(main())
