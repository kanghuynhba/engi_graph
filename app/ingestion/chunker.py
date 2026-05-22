import re


class Chunker:
    def split(self, clean_text: str, chunk_size: int = 500, chunk_overlap: int = 50) -> list[str]:
        paragraphs = [p.strip() for p in clean_text.split("\n\n") if p.strip()]
        units: list[list[str]] = []
        for paragraph in paragraphs:
            words = paragraph.split()
            if len(words) <= chunk_size:
                units.append(words)
                continue
            for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
                words = sentence.split()
                if words:
                    units.append(words)

        chunks: list[list[str]] = []
        current: list[str] = []
        for unit in units:
            if current and len(current) + len(unit) > chunk_size:
                chunks.append(current)
                overlap = current[-chunk_overlap:] if chunk_overlap > 0 else []
                current = overlap + unit
            else:
                current.extend(unit)
        if current:
            chunks.append(current)
        return [" ".join(chunk) for chunk in chunks]
