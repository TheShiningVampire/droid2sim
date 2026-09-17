"""Repository-relative paths shared by the CLI, scripts, and tests."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EPISODE = ROOT / "data" / "episode"
DEFAULT_OUTPUT = ROOT / "artifacts" / "final"


def resolve_output(path: str | Path) -> Path:
    """Resolve relative output paths against the repository, not the shell cwd."""
    return ROOT / path
