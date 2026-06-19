from __future__ import annotations

import base64
from pathlib import Path


def image_to_base64(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None

    mime = "image/png"
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        mime = "image/jpeg"
    elif path.suffix.lower() == ".webp":
        mime = "image/webp"

    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime};base64,{encoded}"
