import uvicorn
from fastapi import FastAPI

from common import install_requests_cache, prepare, find_paths_for_fiat

app = FastAPI()
install_requests_cache()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/best-rates")
async def best_path_cli(currency_from: str, currency_to: str, max_length: int = 2, amount: float = 1):
    """Return best conversion paths."""
    graph = prepare()
    paths = find_paths_for_fiat(currency_from, currency_to, graph, max_length)
    return paths

if __name__ == '__main__':
    uvicorn.run(app)
