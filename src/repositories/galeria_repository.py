from __future__ import annotations

from pathlib import Path
from typing import Any

from src.core.database import get_service_client
from src.core.settings import get_settings


TABLE = "galeria_fotos"


def listar_fotos_galeria() -> list[dict[str, Any]]:
    client = get_service_client()
    response = (
        client.table(TABLE)
        .select("id, slot, titulo, storage_path, public_url, atualizado_em")
        .order("slot")
        .execute()
    )
    return response.data or []


def salvar_foto_slot(
    *,
    slot: int,
    file_name: str,
    file_bytes: bytes,
    mime_type: str,
    atualizado_por_email: str | None,
) -> dict[str, Any]:
    """Envia a foto para o Storage e registra/atualiza o slot da galeria."""

    if slot < 1 or slot > 4:
        raise ValueError("Slot inválido. Use valores de 1 a 4.")

    settings = get_settings()
    client = get_service_client()

    extension = Path(file_name).suffix.lower() or ".png"
    storage_path = f"galeria/slot_{slot}{extension}"

    # Bucket precisa existir antes do upload. O schema.sql já cria o bucket.
    bucket = client.storage.from_(settings.gallery_bucket)
    file_options = {
        "content-type": mime_type,
        "upsert": "true",
    }

    try:
        bucket.upload(
            path=storage_path,
            file=file_bytes,
            file_options=file_options,
        )
    except Exception:
        # Alguns ambientes ignoram o upsert no upload. Nesse caso, substitui o arquivo.
        bucket.update(
            path=storage_path,
            file=file_bytes,
            file_options=file_options,
        )

    public_url_response = bucket.get_public_url(storage_path)
    public_url = str(public_url_response)

    payload = {
        "slot": slot,
        "titulo": f"Foto {slot}",
        "storage_path": storage_path,
        "public_url": public_url,
        "mime_type": mime_type,
        "atualizado_por_email": atualizado_por_email,
    }

    response = (
        client.table(TABLE)
        .upsert(payload, on_conflict="slot")
        .execute()
    )
    return (response.data or [payload])[0]
