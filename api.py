import uvicorn
from fastapi import FastAPI

from common import install_requests_cache, prepare, find_paths_for_fiat, prepare_conversion_paths

app = FastAPI()
install_requests_cache()

@app.get("/")
async def root():
    return {"message": "Hello World"}


# TODO: rename max_length to 'hops'
@app.get("/best-rates/{currency_from}-{currency_to}")
async def best_path_cli(currency_from: str, currency_to: str, hops: int = 4, amount: float = 1):
    """Return best conversion paths."""
    graph = prepare()
    hops = min(hops, 4)
    paths = find_paths_for_fiat(currency_from, currency_to, graph, hops)
    print(f'Found {len(paths)} paths to convert (Displaying top 10)')
    conversion_paths = prepare_conversion_paths(paths, amount)
    return conversion_paths[:10]

if __name__ == '__main__':
    uvicorn.run(app)
