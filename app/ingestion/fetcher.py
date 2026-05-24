import certifi
import httpx


class AsyncHTMLFetcher:
    def __init__(self, client: httpx.AsyncClient | None = None):
        self.client = client

    async def fetch(self, url: str) -> tuple[str, str]:
        headers = {
            "User-Agent": "EngiGraph/1.0 (+https://github.com/engigraph)"
        }

        if self.client:
            response = await self.client.get(
                url,
                headers=headers,
                follow_redirects=True,
            )
        else:
            async with httpx.AsyncClient(
                timeout=30.0,
                verify=certifi.where(),
            ) as client:
                response = await client.get(
                    url,
                    headers=headers,
                    follow_redirects=True,
                )

        response.raise_for_status()
        return response.text, str(response.url)
