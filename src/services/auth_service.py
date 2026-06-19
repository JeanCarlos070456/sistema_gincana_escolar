from __future__ import annotations

from src.core.database import get_anon_client
from src.core.settings import get_settings


def autenticar_diretora_por_senha(password: str) -> tuple[bool, str]:
    """Autentica a diretora no Supabase Auth usando e-mail fixo do secrets.

    A UI pede apenas a senha. O e-mail institucional fica protegido no servidor.
    """

    if not password or not password.strip():
        return False, "Informe a senha de acesso."

    settings = get_settings()
    client = get_anon_client()

    try:
        response = client.auth.sign_in_with_password(
            {
                "email": settings.director_email,
                "password": password,
            }
        )
    except Exception:
        return False, "Senha inválida ou usuário não encontrado no Supabase Auth."

    if not getattr(response, "user", None):
        return False, "Não foi possível autenticar o acesso."

    return True, settings.director_email
