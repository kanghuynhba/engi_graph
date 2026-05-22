from abc import ABC, abstractmethod
from datetime import datetime

from app.domain.results import ArticleExtractionResult


class ExtractionError(Exception):
    pass


class ContentExtractor(ABC):
    @abstractmethod
    def extract(self, html: str, url: str) -> ArticleExtractionResult:
        raise NotImplementedError


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
    except ValueError:
        return None


class TrafilaturaExtractor(ContentExtractor):
    def extract(self, html: str, url: str) -> ArticleExtractionResult:
        import trafilatura

        metadata = trafilatura.extract_metadata(html)
        text = trafilatura.extract(html, include_comments=False, include_tables=False) or ""
        return ArticleExtractionResult(
            url=url,
            canonical_url=getattr(metadata, "url", None) if metadata else None,
            title=getattr(metadata, "title", None) if metadata else None,
            author_name=getattr(metadata, "author", None) if metadata else None,
            published_at=_parse_date(getattr(metadata, "date", None) if metadata else None),
            updated_at=None,
            raw_text=text,
            excerpt=getattr(metadata, "description", None) if metadata else None,
            language=getattr(metadata, "language", None) if metadata else None,
        )


class BeautifulSoupExtractor(ContentExtractor):
    def extract(self, html: str, url: str) -> ArticleExtractionResult:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        title = self._meta(soup, "og:title") or (soup.title.string.strip() if soup.title and soup.title.string else None)
        excerpt = self._meta(soup, "og:description") or self._meta_name(soup, "description")
        canonical = soup.find("link", rel="canonical")
        canonical_url = canonical.get("href") if canonical else None
        published = self._meta(soup, "article:published_time") or self._meta_name(soup, "date")
        author_name = self._meta(soup, "article:author") or self._meta_name(soup, "author")
        container = soup.find("article") or soup.find("main") or soup.body
        texts = [node.get_text(" ", strip=True) for node in container.find_all(["h1", "h2", "h3", "p", "li"])] if container else []
        return ArticleExtractionResult(
            url=url,
            canonical_url=canonical_url,
            title=title,
            author_name=author_name,
            published_at=_parse_date(published),
            updated_at=None,
            raw_text="\n\n".join(text for text in texts if text),
            excerpt=excerpt,
            language=soup.html.get("lang") if soup.html else None,
        )

    def _meta(self, soup, property_name: str) -> str | None:
        tag = soup.find("meta", property=property_name)
        return tag.get("content") if tag else None

    def _meta_name(self, soup, name: str) -> str | None:
        tag = soup.find("meta", attrs={"name": name})
        return tag.get("content") if tag else None


class FallbackContentExtractor(ContentExtractor):
    def __init__(self) -> None:
        self.extractors = [TrafilaturaExtractor(), BeautifulSoupExtractor()]

    def extract(self, html: str, url: str) -> ArticleExtractionResult:
        last_result = None
        for extractor in self.extractors:
            try:
                result = extractor.extract(html, url)
                if len(result.raw_text.strip()) >= 200:
                    return result
                last_result = result
            except Exception:
                continue
        if last_result:
            raise ExtractionError(f"Extracted content too short for {url}")
        raise ExtractionError(f"Could not extract article content from {url}")
