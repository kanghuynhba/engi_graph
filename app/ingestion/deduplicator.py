import hashlib
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse


class Deduplicator:
    def hash_content(self, text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        query = [(key, value) for key, value in parse_qsl(parsed.query) if not key.lower().startswith("utm_")]
        path = parsed.path.rstrip("/") or "/"
        return urlunparse((parsed.scheme.lower(), parsed.netloc.lower(), path, "", urlencode(query), ""))
