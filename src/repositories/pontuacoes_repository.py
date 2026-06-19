from __future__ import annotations

from typing import Any

from src.core.database import get_service_client


def inserir_lancamentos(lancamentos: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not lancamentos:
        return []

    supabase = get_service_client()

    response = (
        supabase
        .table("pontuacoes")
        .insert(lancamentos)
        .execute()
    )

    return response.data or []


def listar_lancamentos(limit: int = 200) -> list[dict[str, Any]]:
    supabase = get_service_client()

    response = (
        supabase
        .table("pontuacoes")
        .select(
            "id, data_lancamento, observacao, turma_id, provas, prendas, pontos, criado_por_email"
        )
        .order("data_lancamento", desc=True)
        .limit(limit)
        .execute()
    )

    return response.data or []


def atualizar_lancamento(
    *,
    lancamento_id: str,
    data_lancamento: str,
    observacao: str | None,
    turma_id: str,
    provas: int,
    prendas: int,
) -> dict[str, Any] | None:
    supabase = get_service_client()

    total = int(provas or 0) + int(prendas or 0)

    payload = {
        "data_lancamento": data_lancamento,
        "observacao": observacao or None,
        "turma_id": turma_id,
        "provas": int(provas or 0),
        "prendas": int(prendas or 0),
        "pontos": total,
    }

    response = (
        supabase
        .table("pontuacoes")
        .update(payload)
        .eq("id", lancamento_id)
        .execute()
    )

    data = response.data or []

    if not data:
        return None

    return data[0]