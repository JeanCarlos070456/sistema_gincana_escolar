from __future__ import annotations

from datetime import date

import streamlit as st

from src.core.session import (
    get_director_email,
    is_director_authenticated,
    logout_director,
    set_director_authenticated,
)
from src.services.auth_service import autenticar_diretora_por_senha
from src.services.galeria_service import atualizar_foto_galeria
from src.services.pontuacao_service import registrar_pontos_do_dia
from src.services.ranking_service import obter_turmas


@st.dialog("Acesso Diretor")
def render_director_dialog() -> None:
    st.caption("Área restrita para lançamento diário de provas, prendas e atualização da galeria.")

    if not is_director_authenticated():
        _render_login()
        return

    _render_update_form()


def _render_login() -> None:
    senha = st.text_input(
        "Senha",
        type="password",
        placeholder="Digite a senha da diretora",
    )

    col1, col2 = st.columns([1, 1])

    with col1:
        entrar = st.button("Entrar", use_container_width=True)

    with col2:
        fechar = st.button("Cancelar", use_container_width=True)

    if fechar:
        st.rerun()

    if entrar:
        ok, result = autenticar_diretora_por_senha(senha)

        if not ok:
            st.error(result)
            return

        set_director_authenticated(result)
        st.success("Acesso liberado.")
        st.rerun()


def _render_update_form() -> None:
    turmas = obter_turmas()
    email = get_director_email()

    if not turmas:
        st.error("Nenhuma turma ativa encontrada. Confira a tabela turmas no Supabase.")
        return

    st.success(f"Acesso autenticado: {email}")

    with st.form("form_lancamento_diario", clear_on_submit=True):
        st.subheader("Lançamento diário")

        data_lancamento = st.date_input("Data do lançamento", value=date.today())

        observacao = st.text_area(
            "Observação do dia",
            placeholder="Ex.: pescaria, prendas, quadrilha, brinquedos, atividades...",
        )

        st.divider()

        dados_por_turma: dict[str, dict[str, int]] = {}

        for turma in turmas:
            turma_id = turma["id"]
            turma_nome = turma["nome"]

            st.markdown(f"### {turma_nome}")

            col_provas, col_prendas = st.columns(2)

            with col_provas:
                provas = st.number_input(
                    "Provas",
                    min_value=0,
                    max_value=999999,
                    value=0,
                    step=1,
                    key=f"provas_{turma_id}",
                )

            with col_prendas:
                prendas = st.number_input(
                    "Prendas",
                    min_value=0,
                    max_value=999999,
                    value=0,
                    step=1,
                    key=f"prendas_{turma_id}",
                )

            st.info(f"Total do dia para {turma_nome}: {int(provas) + int(prendas)} ponto(s)")

            dados_por_turma[turma_id] = {
                "provas": int(provas),
                "prendas": int(prendas),
            }

            st.divider()

        st.subheader("Atualizar galeria de fotos")
        st.caption("Envie até 4 imagens. Só os slots preenchidos serão atualizados.")

        uploads = {}

        upload_cols = st.columns(4)

        for slot in range(1, 5):
            with upload_cols[slot - 1]:
                uploads[slot] = st.file_uploader(
                    f"Foto {slot}",
                    type=["png", "jpg", "jpeg", "webp"],
                    key=f"foto_slot_{slot}",
                )

        salvar = st.form_submit_button("Salvar lançamento", use_container_width=True)

    col_sair, col_fechar = st.columns(2)

    with col_sair:
        if st.button("Sair do acesso", use_container_width=True):
            logout_director()
            st.rerun()

    with col_fechar:
        if st.button("Fechar", use_container_width=True):
            st.rerun()

    if not salvar:
        return

    try:
        registros = registrar_pontos_do_dia(
            dados_por_turma=dados_por_turma,
            data_lancamento=data_lancamento,
            observacao=observacao,
            criado_por_email=email,
        )

        fotos_atualizadas = 0

        for slot, uploaded_file in uploads.items():
            if uploaded_file is not None:
                atualizar_foto_galeria(
                    slot=slot,
                    uploaded_file=uploaded_file,
                    atualizado_por_email=email,
                )

                fotos_atualizadas += 1

        st.cache_data.clear()

        if registros or fotos_atualizadas:
            st.success(
                f"Atualização concluída: {len(registros)} lançamento(s) "
                f"e {fotos_atualizadas} foto(s) atualizada(s)."
            )
            st.rerun()
        else:
            st.info("Nada foi alterado. Informe provas, prendas ou envie novas fotos.")

    except Exception as exc:
        st.error(f"Erro ao salvar atualização: {exc}")