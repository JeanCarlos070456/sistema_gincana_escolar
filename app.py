from __future__ import annotations

import streamlit as st

from src.core.session import init_session_state
from src.core.settings import get_missing_secrets
from src.services.galeria_service import obter_fotos_galeria
from src.services.ranking_service import obter_ranking
from src.ui.admin_dialog import render_director_dialog
from src.ui.components import (
    render_footer,
    render_gallery,
    render_header,
    render_ranking_cards,
)
from src.ui.styles import inject_css


st.set_page_config(
    page_title="Gincana Garatuja",
    page_icon="🌽",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def get_ranking_fallback() -> list[dict]:
    return [
        {
            "id": "fallback-jardim",
            "nome": "Jardim",
            "pontos_total": 0,
            "posicao": 1,
        },
        {
            "id": "fallback-maternal",
            "nome": "Maternal",
            "pontos_total": 0,
            "posicao": 2,
        },
        {
            "id": "fallback-acompanhamento",
            "nome": "Acompanhamento Escolar",
            "pontos_total": 0,
            "posicao": 3,
        },
    ]


def render_supabase_warning(error: Exception | None = None) -> None:
    missing = get_missing_secrets()

    if missing:
        st.warning(
            "Modo visual ativo: o Supabase ainda não foi configurado. "
            "Crie o arquivo `.streamlit/secrets.toml` para ativar banco, login da diretora, pontos e galeria."
        )

        with st.expander("Ver secrets pendentes"):
            st.code("\n".join(missing), language="text")

        return

    st.warning(
        "Não foi possível conectar ao Supabase. "
        "Confira se o schema.sql foi executado e se as chaves do secrets.toml estão corretas."
    )

    if error is not None:
        with st.expander("Ver erro técnico"):
            st.code(str(error), language="text")


def main() -> None:
    init_session_state()
    inject_css()

    st.markdown(
        """
        <div class="director-band">
            <div class="director-band-title">Escola de Educação Infantil Garatuja</div>
            <div class="director-band-subtitle">Sistema de Informação- Gincana Garatuja</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    left_space, center_button, right_space = st.columns([2.2, 1.3, 2.2])
    with center_button:
        if st.button("Acesso Diretor", use_container_width=True):
            render_director_dialog()

    render_header()

    try:
        ranking = obter_ranking()
        fotos = obter_fotos_galeria()

    except Exception as exc:
        render_supabase_warning(exc)
        ranking = get_ranking_fallback()
        fotos = []

    if not ranking:
        st.warning(
            "Ranking vazio. Execute o arquivo `supabase/schema.sql` no Supabase "
            "para criar as turmas iniciais."
        )
        ranking = get_ranking_fallback()

    render_ranking_cards(ranking)
    render_gallery(fotos)
    render_footer()


if __name__ == "__main__":
    main()