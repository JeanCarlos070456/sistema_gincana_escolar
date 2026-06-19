from __future__ import annotations

from datetime import date
from typing import Any

from src.repositories.pontuacoes_repository import inserir_lancamentos


def registrar_pontos_do_dia(
    *,
    dados_por_turma: dict[str, dict[str, int]],
    data_lancamento: date,
    observacao: str | None,
    criado_por_email: str | None,
) -> list[dict[str, Any]]:
    """
    Cria lançamentos diários acumulativos.

    Regras:
    - provas: pontos das provas do dia.
    - prendas: pontos das prendas do dia.
    - total: calculado no banco como provas + prendas.
    - pontos: mantido por compatibilidade com a versão anterior.
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