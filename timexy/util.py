from pathlib import Path
from typing import Callable, Dict, Iterable, Union


def ensure_path(path: Union[str, Path]) -> Path:
    if isinstance(path, str):
        return Path(path)
    else:
        return path


def to_disk(
    path: Union[str, Path],
    writers: Dict[str, Callable[[Path], None]],
    exclude: Iterable[str],
) -> Path:
    path = ensure_path(path)
    if not path.exists():
        path.mkdir()
    for key, writer in writers.items():
        # Split to support file names like meta.json
        if key.split(".")[0] not in exclude:
            writer(path / key)
    return path


def from_disk(
    path: Union[str, Path],
    readers: Dict[str, Callable[[Path], None]],
    exclude: Iterable[str],
) -> Path:
    path = ensure_path(path)
    for key, reader in readers.items():
        # Split to support file names like meta.json
        if key.split(".")[0] not in exclude:
            reader(path / key)
    return path


def parse_timex3(timex3str: str) -> Dict:
    return {
        e.split("=")[0]: e.split("=")[1]
        for e in timex3str[len("TIMEX3 ") :].replace('"', "").split()
    }
