from __future__ import annotations

from datetime import date, datetime
from typing import Any

import streamlit as st

from src.repositories.pontuacoes_repository import (
    atualizar_lancamento,
    inserir_lancamentos,
    listar_lancamentos,
)


def registrar_pontos_do_dia(
    *,
    dados_por_turma: dict[str, dict[str, int]],
    data_lancamento: date,
    observacao: str | None,
    criado_por_email: str | None,
) -> list[dict[str, Any]]:
    """
    Cria lançamentos diários acumulativos.

    Cada turma recebe um novo registro.
    O ranking soma Provas + Prendas no histórico inteiro.
    Registros totalmente zerados são ignorados para não poluir o banco.
    """

    lancamentos: list[dict[str, Any]] = []

    for turma_id, valores in dados_por_turma.items():
        provas = int(valores.get("provas") or 0)
        prendas = int(valores.get("prendas") or 0)
        total = provas + prendas

        if total <= 0:
            continue

        lancamentos.append(
            {
                "turma_id": turma_id,
                "pontos": total,
                "provas": provas,
                "prendas": prendas,
                "data_lancamento": str(data_lancamento),
                "observacao": observacao or None,
                "criado_por_email": criado_por_email,
            }
        )

    return inserir_lancamentos(lancamentos)


@st.cache_data(ttl=20, show_spinner=False)
def obter_lancamentos_para_edicao(limit: int = 200) -> list[dict[str, Any]]:
    return listar_lancamentos(limit=limit)


def salvar_edicoes_lancamentos(lancamentos_editados: list[dict[str, Any]]) -> int:
    atualizados = 0

    for item in lancamentos_editados:
        lancamento_id = str(item["id"]).strip()

        if not lancamento_id:
            continue

        resultado = atualizar_lancamento(
            lancamento_id=lancamento_id,
            data_lancamento=_normalizar_data(item.get("data_lancamento")),
            observacao=str(item.get("observacao") or "").strip() or None,
            turma_id=str(item.get("turma_id") or "").strip(),
            provas=max(0, int(item.get("provas") or 0)),
            prendas=max(0, int(item.get("prendas") or 0)),
        )

        if resultado:
            atualizados += 1

    if atualizados:
        st.cache_data.clear()

    return atualizados


def _normalizar_data(value: Any) -> str:
    if isinstance(value, datetime):
        return value.date().isoformat()

    if isinstance(value, date):
        return value.isoformat()

    texto = str(value or "").strip()

    if not texto:
        return date.today().isoformat()

    try:
        return datetime.fromisoformat(texto[:10]).date().isoformat()
    except Exception:
        pass

    try:
        return datetime.strptime(texto, "%d/%m/%Y").date().isoformat()
    except Exception:
        return date.today().isoformat()