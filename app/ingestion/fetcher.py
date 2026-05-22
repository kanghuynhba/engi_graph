import httpx


class FetchError(Exception):
    pass


class AsyncHTMLFetcher:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def fetch(self, url: str) -> tuple[str, str]:
        headers = {"User-Agent": "EngiGraph/1.0 (+https://github.com/engigraph)"}
        try:
            response = await self.client.get(url, headers=headers, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise FetchError(f"HTTP error fetching {url}: {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            raise FetchError(f"HTTP error fetching {url}: {exc}") from exc
        return response.text, str(response.url)
