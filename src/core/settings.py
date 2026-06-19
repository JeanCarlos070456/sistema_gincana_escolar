from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT_DIR / "assets"

SUPPORTED_IMAGE_EXTENSIONS = [".png", ".jpg", ".jpeg", ".webp"]


def find_asset_image(base_name: str) -> Path:
    """
    Procura automaticamente uma imagem dentro da pasta assets.

    Exemplo:
    find_asset_image("mascotes") aceita:
    - assets/mascotes.png
    - assets/mascotes.jpg
    - assets/mascotes.jpeg
    - assets/mascotes.webp
    """

    for extension in SUPPORTED_IMAGE_EXTENSIONS:
        candidate = ASSETS_DIR / f"{base_name}{extension}"

        if candidate.exists() and candidate.is_file():
            return candidate

    return ASSETS_DIR / f"{base_name}.png"


LOGO_PATH = find_asset_image("logo")
MASCOTES_PATH = find_asset_image("mascotes")


@dataclass(frozen=True)
class AppSettings:
    supabase_url: str
    supabase_anon_key: str
    supabase_service_role_key: str
    director_email: str
    gallery_bucket: str = "galeria-junina"


def _read_secret(key: str) -> str | None:
    """
    Lê uma chave do secrets.toml sem quebrar o app quando o arquivo ainda não existe.
    """

    try:
        value = st.secrets.get(key)
    except Exception:
        return None

    if value is None:
        return None

    value = str(value).strip()
    return value or None


def get_missing_secrets() -> list[str]:
    """
    Retorna quais secrets obrigatórios ainda não foram configurados.
    Usado pelo app.py para exibir aviso limpo em vez de traceback.
    """

    required_keys = [
        "SUPABASE_URL",
        "SUPABASE_ANON_KEY",
        "SUPABASE_SERVICE_ROLE_KEY",
        "DIRECTOR_EMAIL",
    ]

    return [key for key in required_keys if not _read_secret(key)]


def has_supabase_config() -> bool:
    """
    Verifica se o Supabase já está configurado.
    """

    return len(get_missing_secrets()) == 0


@st.cache_resource(show_spinner=False)
def get_settings() -> AppSettings:
    """
    Centraliza leitura de secrets para evitar credenciais espalhadas no código.
    """

    missing = get_missing_secrets()

    if missing:
        raise RuntimeError(
            "Secrets ausentes: "
            + ", ".join(missing)
            + ". Configure .streamlit/secrets.toml antes de executar."
        )

    return AppSettings(
        supabase_url=_read_secret("SUPABASE_URL") or "",
        supabase_anon_key=_read_secret("SUPABASE_ANON_KEY") or "",
        supabase_service_role_key=_read_secret("SUPABASE_SERVICE_ROLE_KEY") or "",
        director_email=_read_secret("DIRECTOR_EMAIL") or "",
        gallery_bucket=_read_secret("SUPABASE_GALLERY_BUCKET") or "galeria-junina",
    )