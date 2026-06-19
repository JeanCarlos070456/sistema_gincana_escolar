from __future__ import annotations

import streamlit as st


DIRECTOR_AUTH_KEY = "director_authenticated"
DIRECTOR_EMAIL_KEY = "director_email"


def init_session_state() -> None:
    st.session_state.setdefault(DIRECTOR_AUTH_KEY, False)
    st.session_state.setdefault(DIRECTOR_EMAIL_KEY, None)


def set_director_authenticated(email: str) -> None:
    st.session_state[DIRECTOR_AUTH_KEY] = True
    st.session_state[DIRECTOR_EMAIL_KEY] = email


def logout_director() -> None:
    st.session_state[DIRECTOR_AUTH_KEY] = False
    st.session_state[DIRECTOR_EMAIL_KEY] = None


def is_director_authenticated() -> bool:
    return bool(st.session_state.get(DIRECTOR_AUTH_KEY))


def get_director_email() -> str | None:
    return st.session_state.get(DIRECTOR_EMAIL_KEY)
