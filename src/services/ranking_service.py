from __future__ import annotations

from typing import Any

import streamlit as st

from src.repositories.turmas_repository import listar_ranking, listar_turmas_ativas


@st.cache_data(ttl=20, show_spinner=False)
def obter_ranking() -> list[dict[str, Any]]:
    ranking = listar_ranking()
    return ranking


@st.cache_data(ttl=60, show_spinner=False)
def obter_turmas() -> list[dict[str, Any]]:
    return listar_turmas_ativas()


def formatar_posicao(posicao: int) -> str:
    mapa = {
        1: "1º lugar",
        2: "2º lugar",
        3: "3º lugar",
    }
    return mapa.get(int(posicao), f"{posicao}º lugar")


def medalha_por_posicao(posicao: int) -> str:
    return {
        1: "🥇",
        2: "🥈",
        3: "🥉",
    }.get(int(posicao), "🎯")
