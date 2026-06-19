from __future__ import annotations

from typing import Any

from src.core.database import get_service_client


def listar_ranking() -> list[dict[str, Any]]:
    """
    Busca o ranking consolidado pela view public.ranking_turmas.
    A view já soma todos os lançamentos da tabela pontuacoes.
    """

    supabase = get_service_client()

    response = (
        supabase
        .table("ranking_turmas")
        .select("*")
        .order("posicao")
        .execute()
    )

    return response.data or []


def listar_turmas_ativas() -> list[dict[str, Any]]:
    """
    Lista somente as turmas ativas.

    Atenção:
    No schema do banco, a coluna correta é 'ativo', não 'ativa'.
    """

    supabase = get_service_client()

    response = (
        supabase
        .table("turmas")
        .select("id, nome, slug, ordem, ativo")
        .eq("ativo", True)
        .order("ordem")
        .execute()
    )

    return response.data or []