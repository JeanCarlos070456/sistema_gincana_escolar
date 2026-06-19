from __future__ import annotations

import streamlit as st
from supabase import Client, create_client

from src.core.settings import get_settings


@st.cache_resource(show_spinner=False)
def get_anon_client() -> Client:
    """Cliente usado somente para autenticação via Supabase Auth."""

    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_anon_key)


@st.cache_resource(show_spinner=False)
def get_service_client() -> Client:
    """Cliente servidor usado para consultas, inserts e uploads.

    A service_role_key precisa ficar exclusivamente em secrets.toml.
    Não commitar essa chave em repositório.
    """

    settings = get_settings()
    return create_client(settings.supabase_url, settings.supabase_service_role_key)
