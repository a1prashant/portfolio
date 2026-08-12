from __future__ import annotations

import base64
import re
from pathlib import Path
from urllib.parse import unquote, urlparse

import requests


DATA_URI_RE = re.compile(r"^data:image/([^;]+);base64,(.+)$", re.DOTALL)


class ImageHandler:
    """Resolve local images and optionally download remote images."""

    def __init__(self, document_dir: Path, cache_dir: Path, allow_remote: bool = True):
        self.document_dir = Path(document_dir)
        self.cache_dir = Path(cache_dir)
        self.allow_remote = allow_remote
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def resolve(self, src: str) -> Path | None:
        src = src.strip()

        match = DATA_URI_RE.match(src)
        if match:
            ext = match.group(1).split("+")[0]
            target = self.cache_dir / f"data_image.{ext}"
            target.write_bytes(base64.b64decode(match.group(2)))
            return target

        parsed = urlparse(src)
        if parsed.scheme in {"http", "https"}:
            if not self.allow_remote:
                return None
            return self._download(src)

        # Remove URL fragments, unescape Markdown spaces, and decode percent-encoding
        # (e.g. %20 -> space) so paths like ./media_A%20Folder/image.png resolve.
        clean = unquote(src.split("#", 1)[0].replace("\\ ", " "))
        candidate = (self.document_dir / clean).resolve()

        if candidate.exists() and candidate.is_file():
            return candidate

        # Also allow paths relative to the current working directory.
        candidate = Path(clean).expanduser().resolve()
        if candidate.exists() and candidate.is_file():
            return candidate

        return None

    def _download(self, url: str) -> Path | None:
        filename = Path(urlparse(url).path).name or "remote_image"
        safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", filename)
        target = self.cache_dir / safe_name

        if target.exists():
            return target

        try:
            response = requests.get(
                url,
                timeout=30,
                headers={"User-Agent": "md-to-word/0.1"},
            )
            response.raise_for_status()
            target.write_bytes(response.content)
            return target
        except requests.RequestException:
            return None
