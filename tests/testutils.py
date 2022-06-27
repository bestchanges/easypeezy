from pathlib import Path


def cassette(path: str):
    CASSETTES_PATH = Path(__file__).parent.resolve()
    return str(Path(CASSETTES_PATH, path))
