import sys
from pathlib import Path

# Allow tests to import the spec tooling (tools/ is not a package).
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
