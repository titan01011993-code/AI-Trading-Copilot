from pathlib import Path

CACHE = Path("data/cache")

CACHE.mkdir(
    parents=True,
    exist_ok=True
)