from __future__ import annotations

from html import escape

import streamlit as st

from src.core.settings import LOGO_PATH, MASCOTES_PATH
from src.services.ranking_service import formatar_posicao, medalha_por_posicao
from src.ui.assets import image_to_base64


def render_header() -> None:
    logo_data = image_to_base64(LOGO_PATH)
    mascotes_data = image_to_base64(MASCOTES_PATH)
    flags_html = "".join('<span class="flag"></span>' for _ in range(28))

    logo_html = (
        f'<img class="brand-logo" src="{logo_data}" alt="Logo da escola">'
        if logo_data
        else '<div class="brand-placeholder">logo<br>assets</div>'
    )

    mascotes_html = (
        f'<img class="mascotes-img" src="{mascotes_data}" alt="Mascotes do evento">'
        if mascotes_data
        else '<div class="brand-placeholder mascot-placeholder">mascotes<br>assets</div>'
    )

    html = (
        '<div class="event-hero">'
        '<div class="hero-pattern"></div>'

        '<div class="hero-left">'
        '<div class="brand-logo-frame">'
        f'{logo_html}'
        '</div>'

        '<div class="title-wrap">'
        '<div class="hero-eyebrow">🎉 Festa Junina Garatuja</div>'
        '<h1>Gincana Garatuja</h1>'
        '<p>Placar acumulado das turmas em tempo real</p>'

        '<div class="hero-tags">'
        '<span>🌽 Provas</span>'
        '<span>🎁 Prendas</span>'
        '<span>🏆 Ranking Geral</span>'
        '</div>'

        '</div>'
        '</div>'

        '<div class="hero-right">'
        '<div class="mascot-stage">'
        f'{mascotes_html}'
        '</div>'
        '</div>'

        '</div>'

        '<div class="bandeirinhas">'
        '<div class="flag-row">'
        f'{flags_html}'
        '</div>'
        '</div>'
    )

    st.markdown(html, unsafe_allow_html=True)


def render_ranking_cards(ranking: list[dict]) -> None:
    st.markdown(
        (
            '<div class="section-heading">'
            '<div class="section-kicker">Placar oficial</div>'
            '<div class="ranking-section-title">🏆 Classificação geral</div>'
            '<p>O ranking é definido pelo total acumulado de provas + prendas.</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    cards = []

    for row in ranking:
        posicao = int(row.get("posicao") or 0)
        nome = escape(str(row.get("nome", "Turma")))

        total = int(row.get("pontos_total") or 0)
        provas = int(row.get("provas_total") or 0)
        prendas = int(row.get("prendas_total") or 0)

        posicao_texto = escape(formatar_posicao(posicao))
        medalha = medalha_por_posicao(posicao)

        total_formatado = f"{total:,}".replace(",", ".")
        provas_formatado = f"{provas:,}".replace(",", ".")
        prendas_formatado = f"{prendas:,}".replace(",", ".")

        card_html = (
            f'<article class="turma-card rank-{posicao}">'
            f'<div class="rank-ribbon">{posicao_texto}</div>'
            f'<div class="card-content">'
            f'<div class="medalha">{medalha}</div>'
            f'<div class="turma-nome">{nome}</div>'
            f'<div class="turma-total-label">Total acumulado</div>'
            f'<div class="turma-pontos">{total_formatado}</div>'
            f'<div class="turma-pontos-label">pontos no ranking geral</div>'
            f'<div class="turma-breakdown">'
            f'<div class="mini-score provas-score">'
            f'<span>Provas</span>'
            f'<strong>{provas_formatado}</strong>'
            f'</div>'
            f'<div class="mini-score prendas-score">'
            f'<span>Prendas</span>'
            f'<strong>{prendas_formatado}</strong>'
            f'</div>'
            f'</div>'
            f'</div>'
            f'</article>'
        )

        cards.append(card_html)

    html = f'<div class="ranking-grid">{"".join(cards)}</div>'
    st.markdown(html, unsafe_allow_html=True)


@st.dialog("Foto da gincana")
def render_foto_expandida(url: str, slot: int) -> None:
    st.markdown(
        (
            '<div class="photo-dialog-title">'
            f'📸 Foto {slot} da Gincana Garatuja'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    st.image(url, use_container_width=True)
    st.caption("Visualização ampliada da foto enviada para a galeria.")


def render_gallery(fotos: list[dict]) -> None:
    st.markdown(
        (
            '<div class="section-heading gallery-heading">'
            '<div class="section-kicker">Memórias do evento</div>'
            '<div class="gallery-title">📸 Galeria de fotos da gincana</div>'
            '<p>Fotos atualizadas pela direção durante as atividades.</p>'
            '</div>'
        ),
        unsafe_allow_html=True,
    )

    fotos_por_slot = {
        int(foto.get("slot")): foto
        for foto in fotos
        if foto.get("slot")
    }

    cols = st.columns(4)

    for slot in range(1, 5):
        foto = fotos_por_slot.get(slot)

        with cols[slot - 1]:
            with st.container(border=True):
                if foto and foto.get("public_url"):
                    url = str(foto["public_url"])

                    st.image(
                        url,
                        caption=f"Foto {slot}",
                        use_container_width=True,
                    )

                    if st.button(
                        "Ampliar imagem",
                        key=f"btn_expandir_foto_{slot}",
                        use_container_width=True,
                    ):
                        render_foto_expandida(url=url, slot=slot)

                else:
                    st.markdown(
                        (
                            '<div class="gallery-empty-native">'
                            '<div class="gallery-empty-icon">📷</div>'
                            f'<div>Foto {slot}</div>'
                            '<small>Aguardando envio</small>'
                            '</div>'
                        ),
                        unsafe_allow_html=True,
                    )


def render_footer() -> None:
    st.markdown(
        (
            '<footer class="footer-note">'
            '<span>🌽 Gincana Garatuja</span>'
            '<strong>Atualize provas e prendas diariamente pelo Acesso Diretor.</strong>'
            '</footer>'
        ),
        unsafe_allow_html=True,
    )