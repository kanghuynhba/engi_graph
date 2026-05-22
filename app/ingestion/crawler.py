import json
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

import httpx

from app.models.source import Source


NON_ARTICLE_PATH_PARTS = ("/tag/", "/author/", "/page/", "/search/", "/login/", "/admin/")


class Crawler:
    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def discover_urls(self, source: Source) -> list[str]:
        if source.crawl_mode == "feed":
            return await self._crawl_feed(source.feed_url)
        if source.crawl_mode == "html_index":
            return await self._crawl_html_index(source.base_url, source.allowed_domains)
        if source.crawl_mode == "sitemap":
            return await self._crawl_sitemap(source.sitemap_url)
        if source.crawl_mode == "manual":
            return []
        raise ValueError(f"Unsupported crawl_mode: {source.crawl_mode}")

    async def _crawl_feed(self, feed_url: str | None) -> list[str]:
        if not feed_url:
            return []
        import feedparser

        response = await self.client.get(feed_url, follow_redirects=True)
        response.raise_for_status()
        parsed = feedparser.parse(response.text)
        return self._dedupe(entry.link for entry in parsed.entries if getattr(entry, "link", None))

    async def _crawl_html_index(self, base_url: str, allowed_domains_json: str) -> list[str]:
        from bs4 import BeautifulSoup

        allowed_domains = set(json.loads(allowed_domains_json or "[]"))
        response = await self.client.get(base_url, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        urls = []
        for anchor in soup.find_all("a", href=True):
            url = urljoin(str(response.url), anchor["href"])
            parsed = urlparse(url)
            if parsed.netloc not in allowed_domains:
                continue
            if any(part in parsed.path for part in NON_ARTICLE_PATH_PARTS):
                continue
            if parsed.scheme in {"http", "https"}:
                urls.append(url)
        return self._dedupe(urls)

    async def _crawl_sitemap(self, sitemap_url: str | None) -> list[str]:
        if not sitemap_url:
            return []
        response = await self.client.get(sitemap_url, follow_redirects=True)
        response.raise_for_status()
        root = ElementTree.fromstring(response.text)
        urls = []
        for loc in root.iter():
            if loc.tag.endswith("loc") and loc.text:
                urls.append(loc.text.strip())
        return self._dedupe(urls)

    def _dedupe(self, urls) -> list[str]:
        seen = set()
        deduped = []
        for url in urls:
            if url not in seen:
                seen.add(url)
                deduped.append(url)
        return deduped
