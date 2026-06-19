from __future__ import annotations

from datetime import date, datetime
from typing import Any

import pandas as pd
import streamlit as st

from src.core.session import (
    get_director_email,
    is_director_authenticated,
    logout_director,
    set_director_authenticated,
)
from src.services.auth_service import autenticar_diretora_por_senha
from src.services.galeria_service import atualizar_foto_galeria
from src.services.pontuacao_service import (
    obter_lancamentos_para_edicao,
    registrar_pontos_do_dia,
    salvar_edicoes_lancamentos,
)
from src.services.ranking_service import obter_turmas


@st.dialog("Acesso Diretor", width="large")
def render_director_dialog() -> None:
    st.caption(
        "Área restrita para lançamento diário, edição das pontuações já registradas "
        "e atualização da galeria."
    )

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
        entrar = st.button("Entrar", width="stretch")

    with col2:
        fechar = st.button("Cancelar", width="stretch")

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

    turma_nome_por_id = {
        str(turma["id"]): str(turma["nome"])
        for turma in turmas
    }

    turma_id_por_nome = {
        str(turma["nome"]): str(turma["id"])
        for turma in turmas
    }

    nomes_turmas = [str(turma["nome"]) for turma in turmas]

    st.success(f"Acesso autenticado: {email}")

    _render_tabela_edicao_pontuacoes(
        turma_nome_por_id=turma_nome_por_id,
        turma_id_por_nome=turma_id_por_nome,
        nomes_turmas=nomes_turmas,
    )

    st.divider()

    with st.form("form_lancamento_diario", clear_on_submit=True):
        st.subheader("Novo lançamento diário")
        st.caption("Informe os pontos do dia por turma. O sistema soma Provas + Prendas automaticamente.")

        data_lancamento = st.date_input(
            "Data do lançamento",
            value=date.today(),
            format="DD/MM/YYYY",
        )

        observacao = st.text_area(
            "Atividade / Observação",
            placeholder="Ex.: pescaria, prendas, quadrilha, brincadeiras, atividades...",
        )

        st.divider()

        dados_por_turma: dict[str, dict[str, int]] = {}

        for turma in turmas:
            turma_id = str(turma["id"])
            turma_nome = str(turma["nome"])

            st.markdown(f"### {turma_nome}")

            col_provas, col_prendas, col_total = st.columns([1, 1, 1])

            with col_provas:
                provas = st.number_input(
                    "Provas",
                    min_value=0,
                    max_value=999999,
                    value=0,
                    step=1,
                    key=f"novo_provas_{turma_id}",
                )

            with col_prendas:
                prendas = st.number_input(
                    "Prendas",
                    min_value=0,
                    max_value=999999,
                    value=0,
                    step=1,
                    key=f"novo_prendas_{turma_id}",
                )

            with col_total:
                st.metric(
                    "Total do dia",
                    int(provas) + int(prendas),
                )

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

        salvar = st.form_submit_button("Salvar lançamento", width="stretch")

    col_sair, col_fechar = st.columns(2)

    with col_sair:
        if st.button("Sair do acesso", width="stretch"):
            logout_director()
            st.rerun()

    with col_fechar:
        if st.button("Fechar", width="stretch"):
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


def _render_tabela_edicao_pontuacoes(
    *,
    turma_nome_por_id: dict[str, str],
    turma_id_por_nome: dict[str, str],
    nomes_turmas: list[str],
) -> None:
    st.subheader("Pontuações já registradas")
    st.caption(
        "Confira os lançamentos antes de adicionar novos pontos. "
        "Clique em editar para alterar registros existentes."
    )

    try:
        lancamentos = obter_lancamentos_para_edicao(limit=200)
    except Exception as exc:
        st.warning(f"Não foi possível carregar a tabela de pontuações: {exc}")
        return

    if not lancamentos:
        st.info("Ainda não existem pontuações registradas.")
        return

    df = _montar_dataframe_lancamentos(
        lancamentos=lancamentos,
        turma_nome_por_id=turma_nome_por_id,
    )

    if df.empty:
        st.info("Ainda não existem pontuações registradas.")
        return

    tabela_visual = df.reset_index(drop=True).copy()
    tabela_visual["Data"] = tabela_visual["Data"].apply(_formatar_data_br)

    st.dataframe(
        tabela_visual[["Data", "Atividade", "Turma", "Provas", "Prendas"]],
        hide_index=True,
        width="stretch",
    )

    with st.expander("✏️ Editar pontuações já registradas", expanded=False):
        st.caption(
            "Altere data, atividade, turma, provas ou prendas. "
            "Depois clique em Salvar alteração para substituir no banco."
        )

        editor_df = df.copy()

        resultado = st.data_editor(
            editor_df,
            hide_index=True,
            num_rows="fixed",
            width="stretch",
            column_config={
                "ID": None,
                "Data": st.column_config.DateColumn(
                    "Datas",
                    format="DD/MM/YYYY",
                    required=True,
                ),
                "Atividade": st.column_config.TextColumn(
                    "Atividade",
                    max_chars=300,
                ),
                "Turma": st.column_config.SelectboxColumn(
                    "Turma",
                    options=nomes_turmas,
                    required=True,
                ),
                "Provas": st.column_config.NumberColumn(
                    "Provas",
                    min_value=0,
                    max_value=999999,
                    step=1,
                    required=True,
                ),
                "Prendas": st.column_config.NumberColumn(
                    "Prendas",
                    min_value=0,
                    max_value=999999,
                    step=1,
                    required=True,
                ),
            },
            key="editor_pontuacoes_diretora",
        )

        salvar_alteracoes = st.button(
            "Salvar alteração",
            type="primary",
            width="stretch",
            key="btn_salvar_alteracoes_pontuacoes",
        )

        if not salvar_alteracoes:
            return

        try:
            payload = _converter_editor_para_payload(
                resultado,
                turma_id_por_nome=turma_id_por_nome,
            )

            atualizados = salvar_edicoes_lancamentos(payload)

            if atualizados:
                st.success(f"{atualizados} registro(s) atualizado(s) com sucesso.")
                st.rerun()

            st.info("Nenhuma alteração foi salva.")

        except Exception as exc:
            st.error(f"Erro ao salvar alterações: {exc}")


def _montar_dataframe_lancamentos(
    *,
    lancamentos: list[dict[str, Any]],
    turma_nome_por_id: dict[str, str],
) -> pd.DataFrame:
    linhas: list[dict[str, Any]] = []

    for item in lancamentos:
        lancamento_id = str(item.get("id") or "").strip()

        if not lancamento_id:
            continue

        turma_id = str(item.get("turma_id") or "").strip()
        turma_nome = turma_nome_por_id.get(turma_id, turma_id or "Turma não encontrada")

        provas = int(item.get("provas") or 0)
        prendas = int(item.get("prendas") or 0)

        linhas.append(
            {
                "ID": lancamento_id,
                "Data": _parse_data(item.get("data_lancamento")),
                "Atividade": str(item.get("observacao") or ""),
                "Turma": turma_nome,
                "Provas": provas,
                "Prendas": prendas,
            }
        )

    return pd.DataFrame(linhas)


def _converter_editor_para_payload(
    df: pd.DataFrame,
    *,
    turma_id_por_nome: dict[str, str],
) -> list[dict[str, Any]]:
    payload: list[dict[str, Any]] = []

    for _, row in df.iterrows():
        lancamento_id = str(row.get("ID") or "").strip()
        turma_nome = str(row.get("Turma") or "").strip()
        turma_id = turma_id_por_nome.get(turma_nome)

        if not lancamento_id:
            continue

        if not turma_id:
            raise ValueError(f"Turma inválida ou não encontrada: {turma_nome}")

        payload.append(
            {
                "id": lancamento_id,
                "data_lancamento": _parse_data(row.get("Data")).isoformat(),
                "observacao": str(row.get("Atividade") or "").strip(),
                "turma_id": turma_id,
                "provas": int(row.get("Provas") or 0),
                "prendas": int(row.get("Prendas") or 0),
            }
        )

    return payload


def _parse_data(value: Any) -> date:
    if isinstance(value, datetime):
        return value.date()

    if isinstance(value, date):
        return value

    texto = str(value or "").strip()

    if not texto:
        return date.today()

    try:
        return datetime.fromisoformat(texto[:10]).date()
    except Exception:
        pass

    try:
        return datetime.strptime(texto, "%d/%m/%Y").date()
    except Exception:
        return date.today()


def _formatar_data_br(value: Any) -> str:
    data = _parse_data(value)
    return data.strftime("%d/%m/%Y")