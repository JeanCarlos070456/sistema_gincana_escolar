from __future__ import annotations

from typing import Any

import streamlit as st

from src.repositories.galeria_repository import listar_fotos_galeria, salvar_foto_slot


@st.cache_data(ttl=30, show_spinner=False)
def obter_fotos_galeria() -> list[dict[str, Any]]:
    return listar_fotos_galeria()


def atualizar_foto_galeria(
    *,
    slot: int,
    uploaded_file: Any,
    atualizado_por_email: str | None,
) -> dict[str, Any]:
    if uploaded_file is None:
        raise ValueError("Nenhum arquivo enviado.")

    mime_type = uploaded_file.type or "image/png"
    if mime_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError("Formato inválido. Use PNG, JPG, JPEG ou WEBP.")

    file_bytes = uploaded_file.getvalue()
    if len(file_bytes) > 5 * 1024 * 1024:
        raise ValueError("Imagem muito grande. Limite máximo: 5 MB.")

    return salvar_foto_slot(
        slot=slot,
        file_name=uploaded_file.name,
        file_bytes=file_bytes,
        mime_type=mime_type,
        atualizado_por_email=atualizado_por_email,
    )
