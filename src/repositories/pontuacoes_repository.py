from __future__ import annotations

from typing import Any

from src.core.database import get_service_client


TABLE = "pontuacoes"


def inserir_lancamentos(lancamentos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not lancamentos:
        return []

    client = get_service_client()
    response = client.table(TABLE).insert(lancamentos).execute()
    return response.data or []


def listar_ultimos_lancamentos(limit: int = 10) -> list[dict[str, Any]]:
    client = get_service_client()
    response = (
        client.table(TABLE)
        .select("id, pontos, data_lancamento, observacao, criado_em, turma:turma_id(nome)")
        .order("criado_em", desc=True)
        .limit(limit)
        .execute()
    )
    return response.data or []
