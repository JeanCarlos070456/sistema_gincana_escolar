from __future__ import annotations

import base64
from pathlib import Path

import streamlit as st


ROOT_DIR = Path(__file__).resolve().parents[2]
ASSETS_DIR = ROOT_DIR / "assets"

SUPPORTED_IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def _find_asset_image(base_name: str) -> Path | None:
    for extension in SUPPORTED_IMAGE_EXTENSIONS:
        path = ASSETS_DIR / f"{base_name}{extension}"

        if path.exists() and path.is_file():
            return path

    return None


def _image_to_base64_uri(path: Path | None) -> str | None:
    if path is None:
        return None

    suffix = path.suffix.lower()

    mime_type = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".webp": "image/webp",
    }.get(suffix, "image/png")

    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:{mime_type};base64,{encoded}"


def inject_css() -> None:
    fundo_path = _find_asset_image("fundo")
    fundo_data_uri = _image_to_base64_uri(fundo_path)

    if fundo_data_uri:
        fundo_background_rule = f'background-image: url("{fundo_data_uri}");'
    else:
        fundo_background_rule = "background-image: none;"

    css = """
        <style>
            :root {
                --junina-red: #b83b2e;
                --junina-red-dark: #8f261f;
                --junina-yellow: #f4b942;
                --junina-yellow-soft: #ffe7ad;
                --junina-blue: #22577a;
                --junina-green: #2f7d32;
                --junina-orange: #e87822;
                --paper: #fff8e7;
                --paper-strong: #fff2cc;
                --ink: #3b2f2f;
                --muted: #7a5d42;
                --shadow-soft: 0 18px 45px rgba(79, 52, 28, 0.16);
                --shadow-strong: 0 24px 65px rgba(79, 52, 28, 0.22);
            }

            .stApp {
                position: relative;
                background:
                    radial-gradient(circle at 12% 8%, rgba(244,185,66,.32), transparent 22%),
                    radial-gradient(circle at 88% 12%, rgba(184,59,46,.22), transparent 24%),
                    radial-gradient(circle at 80% 88%, rgba(47,125,50,.18), transparent 26%),
                    radial-gradient(circle at 20% 92%, rgba(34,87,122,.12), transparent 24%),
                    linear-gradient(180deg, #fffaf0 0%, #fff4d6 100%);
                color: var(--ink);
                overflow-x: hidden;
            }

            .stApp:before {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                background-image:
                    linear-gradient(45deg, rgba(184,59,46,.028) 25%, transparent 25%),
                    linear-gradient(-45deg, rgba(34,87,122,.028) 25%, transparent 25%);
                background-size: 46px 46px;
                opacity: .34;
                z-index: 0;
            }

            .stApp:after {
                content: "";
                position: fixed;
                inset: 0;
                pointer-events: none;
                %%FUNDO_BACKGROUND_IMAGE%%
                background-repeat: repeat-y;
                background-position: center 105px;
                background-size: min(1320px, 108vw) auto;
                background-attachment: fixed;
                opacity: .22;
                z-index: 1;
                filter: saturate(1.08) contrast(1.03);
            }

            .stApp > div {
                position: relative;
                z-index: 2;
            }

            header[data-testid="stHeader"] {
                background: transparent;
            }

            [data-testid="stSidebar"] {
                display: none;
            }

            .block-container {
                position: relative;
                z-index: 3;
                padding-top: 1rem;
                padding-bottom: 3rem;
                max-width: 1260px;
            }

            /* FAIXA SUPERIOR / ACESSO DIRETOR */
            .director-band {
                width: 100%;
                text-align: center;
                background:
                    linear-gradient(135deg, rgba(143,38,31,.96), rgba(232,120,34,.96));
                color: white;
                padding: .78rem 1rem .88rem;
                border-radius: 24px;
                box-shadow: 0 14px 34px rgba(184,59,46,.22);
                margin-bottom: .65rem;
                border: 1px solid rgba(255,255,255,.28);
            }

            .director-band-title {
                font-size: 1.06rem;
                font-weight: 950;
                letter-spacing: .35px;
                line-height: 1.1;
            }

            .director-band-subtitle {
                margin-top: .16rem;
                font-size: .86rem;
                font-weight: 600;
                opacity: .94;
            }

            /* BOTÕES */
            div.stButton > button {
                border-radius: 999px;
                border: 0;
                background: linear-gradient(135deg, var(--junina-red), var(--junina-orange));
                color: #fff;
                font-weight: 950;
                font-size: .98rem;
                min-height: 50px;
                box-shadow: 0 10px 24px rgba(184,59,46,.25);
                transition: all .18s ease-in-out;
            }

            div.stButton > button:hover {
                border: 0;
                color: #fff;
                filter: brightness(1.06);
                transform: translateY(-1px);
                box-shadow: 0 14px 28px rgba(184,59,46,.30);
            }

            div.stButton {
                margin-bottom: .7rem;
            }

            /* HERO DO EVENTO */
            .event-hero {
                position: relative;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1.5rem;
                margin-top: .65rem;
                margin-bottom: .65rem;
                padding: 1.25rem 1.35rem;
                border-radius: 34px;
                background:
                    linear-gradient(145deg, rgba(255,255,255,.93), rgba(255,248,231,.985));
                border: 4px solid rgba(244,185,66,.42);
                box-shadow: var(--shadow-soft);
                overflow: hidden;
                backdrop-filter: blur(2px);
            }

            .event-hero:before {
                content: "";
                position: absolute;
                inset: 0;
                background:
                    radial-gradient(circle at 8% 15%, rgba(244,185,66,.30), transparent 18%),
                    radial-gradient(circle at 94% 30%, rgba(184,59,46,.16), transparent 22%),
                    linear-gradient(90deg, rgba(255,255,255,.25), transparent);
                pointer-events: none;
            }

            .hero-pattern {
                position: absolute;
                right: -80px;
                top: -80px;
                width: 260px;
                height: 260px;
                border-radius: 999px;
                background: rgba(244,185,66,.20);
                border: 28px solid rgba(184,59,46,.08);
                pointer-events: none;
            }

            .hero-left,
            .hero-right {
                position: relative;
                z-index: 1;
            }

            .hero-left {
                display: flex;
                align-items: center;
                gap: 1.25rem;
                min-width: 0;
            }

            .brand-logo-frame {
                width: 138px;
                height: 138px;
                flex: 0 0 138px;
                border-radius: 30px;
                background: rgba(255,255,255,.88);
                border: 3px solid rgba(244,185,66,.50);
                display: grid;
                place-items: center;
                box-shadow: 0 14px 28px rgba(79,52,28,.12);
            }

            .brand-logo {
                width: 118px;
                height: 118px;
                object-fit: contain;
                filter: drop-shadow(0 8px 18px rgba(0,0,0,.12));
            }

            .brand-placeholder {
                width: 118px;
                height: 118px;
                border-radius: 24px;
                display: grid;
                place-items: center;
                background: rgba(255,255,255,.78);
                border: 2px dashed rgba(184,59,46,.42);
                color: var(--junina-red);
                font-weight: 950;
                text-align: center;
                line-height: 1.05;
                font-size: .82rem;
            }

            .title-wrap {
                min-width: 0;
            }

            .title-wrap h1 {
                margin: 0;
                font-size: clamp(2.55rem, 4.6vw, 4.35rem);
                line-height: .95;
                color: var(--junina-red);
                text-shadow:
                    2px 3px 0 #ffd36a,
                    5px 7px 0 rgba(0,0,0,.08);
                letter-spacing: -1.8px;
                white-space: nowrap;
            }

            .title-wrap p {
                margin: .5rem 0 0;
                font-size: 1.16rem;
                color: #5b4636;
                font-weight: 850;
            }

            .hero-eyebrow {
                display: inline-flex;
                align-items: center;
                gap: .35rem;
                margin-bottom: .45rem;
                padding: .34rem .72rem;
                border-radius: 999px;
                background: rgba(255,224,163,.82);
                color: #7b4100;
                font-size: .82rem;
                font-weight: 950;
                text-transform: uppercase;
                letter-spacing: .35px;
            }

            .hero-tags {
                display: flex;
                flex-wrap: wrap;
                gap: .5rem;
                margin-top: .85rem;
            }

            .hero-tags span {
                display: inline-flex;
                align-items: center;
                padding: .36rem .68rem;
                border-radius: 999px;
                background: rgba(255,255,255,.78);
                border: 1px solid rgba(119,77,28,.12);
                color: #73523a;
                font-size: .84rem;
                font-weight: 900;
            }

            .hero-right {
                display: grid;
                place-items: center;
            }

            .mascot-stage {
                min-width: 275px;
                min-height: 190px;
                display: grid;
                place-items: center;
                border-radius: 999px;
                background:
                    radial-gradient(circle, rgba(244,185,66,.22), transparent 66%);
            }

            .mascotes-img {
                width: min(360px, 32vw);
                max-height: 245px;
                object-fit: contain;
                filter: drop-shadow(0 16px 24px rgba(0,0,0,.16));
            }

            .mascot-placeholder {
                width: 180px;
                height: 120px;
            }

            /* BANDEIRINHAS */
            .bandeirinhas {
                position: relative;
                height: 44px;
                margin: .05rem 0 1.55rem;
                overflow: hidden;
            }

            .bandeirinhas:before {
                content: "";
                position: absolute;
                left: 0;
                right: 0;
                top: 8px;
                height: 3px;
                background: rgba(80, 50, 20, .32);
            }

            .flag-row {
                display: flex;
                gap: 10px;
                transform: translateY(8px);
                justify-content: center;
            }

            .flag {
                width: 0;
                height: 0;
                border-left: 16px solid transparent;
                border-right: 16px solid transparent;
                border-top: 27px solid var(--junina-red);
                filter: drop-shadow(0 4px 3px rgba(0,0,0,.12));
            }

            .flag:nth-child(2n) { border-top-color: var(--junina-yellow); }
            .flag:nth-child(3n) { border-top-color: var(--junina-blue); }
            .flag:nth-child(4n) { border-top-color: var(--junina-green); }
            .flag:nth-child(5n) { border-top-color: var(--junina-orange); }

            /* TÍTULOS DE SEÇÃO */
            .section-heading {
                text-align: center;
                margin: 1.5rem auto 1.05rem;
            }

            .section-kicker {
                display: inline-flex;
                padding: .28rem .68rem;
                border-radius: 999px;
                background: rgba(255,224,163,.78);
                color: #7b4100;
                font-size: .78rem;
                font-weight: 950;
                text-transform: uppercase;
                letter-spacing: .45px;
                margin-bottom: .35rem;
            }

            .ranking-section-title,
            .gallery-title {
                text-align: center;
                font-weight: 1000;
                color: var(--junina-blue);
                margin: 0;
                font-size: clamp(1.55rem, 3vw, 2rem);
                line-height: 1.1;
            }

            .section-heading p {
                margin: .35rem auto 0;
                max-width: 620px;
                color: var(--muted);
                font-weight: 750;
                font-size: .98rem;
            }

            /* GRID DE RANKING */
            .ranking-grid {
                display: grid;
                grid-template-columns: repeat(3, minmax(220px, 1fr));
                gap: 1.15rem;
                align-items: stretch;
                margin: 0 auto 1.7rem;
            }

            .turma-card {
                position: relative;
                background:
                    linear-gradient(145deg, rgba(255,255,255,.972), rgba(255,248,231,.988));
                border: 4px solid rgba(119, 77, 28, .13);
                border-radius: 32px;
                box-shadow: var(--shadow-soft);
                padding: 1.35rem 1rem 1.15rem;
                min-height: 350px;
                display: flex;
                flex-direction: column;
                justify-content: center;
                text-align: center;
                overflow: hidden;
                transition: transform .18s ease-in-out, box-shadow .18s ease-in-out;
                backdrop-filter: blur(1px);
            }

            .turma-card:hover {
                transform: translateY(-3px);
                box-shadow: var(--shadow-strong);
            }

            .turma-card:before {
                content: "";
                position: absolute;
                inset: 0;
                background-image:
                    linear-gradient(45deg, rgba(184,59,46,.052) 25%, transparent 25%),
                    linear-gradient(-45deg, rgba(34,87,122,.052) 25%, transparent 25%),
                    linear-gradient(45deg, transparent 75%, rgba(244,185,66,.055) 75%),
                    linear-gradient(-45deg, transparent 75%, rgba(47,125,50,.052) 75%);
                background-size: 28px 28px;
                opacity: .72;
                pointer-events: none;
            }

            .turma-card:after {
                content: "";
                position: absolute;
                width: 130px;
                height: 130px;
                right: -45px;
                bottom: -48px;
                border-radius: 999px;
                background: rgba(244,185,66,.15);
                pointer-events: none;
            }

            .turma-card.rank-1 {
                border-color: rgba(244,185,66,.88);
                transform: translateY(-8px);
                box-shadow: 0 28px 68px rgba(142,92,16,.24);
            }

            .turma-card.rank-1:hover {
                transform: translateY(-11px);
            }

            .turma-card.rank-2 {
                border-color: rgba(34,87,122,.34);
            }

            .turma-card.rank-3 {
                border-color: rgba(184,59,46,.34);
            }

            .rank-ribbon {
                position: absolute;
                top: 16px;
                left: 16px;
                z-index: 2;
                padding: .32rem .68rem;
                border-radius: 999px;
                background: #ffe0a3;
                color: #6b3d00;
                font-weight: 1000;
                font-size: .82rem;
                box-shadow: 0 8px 18px rgba(79,52,28,.10);
            }

            .rank-1 .rank-ribbon {
                background: linear-gradient(135deg, #ffe8a8, #f4b942);
                color: #6b3d00;
            }

            .card-content {
                position: relative;
                z-index: 1;
                padding-top: .6rem;
            }

            .medalha {
                font-size: 3.35rem;
                line-height: 1;
                margin-bottom: .42rem;
                filter: drop-shadow(0 6px 10px rgba(0,0,0,.10));
            }

            .turma-nome {
                font-size: clamp(1.42rem, 2.6vw, 2rem);
                font-weight: 1000;
                color: var(--junina-red);
                margin-bottom: .42rem;
                letter-spacing: -.3px;
            }

            .turma-total-label {
                margin-top: .42rem;
                font-size: .85rem;
                font-weight: 1000;
                color: #8a4b00;
                text-transform: uppercase;
                letter-spacing: .72px;
            }

            .turma-pontos {
                font-size: clamp(2.85rem, 5.4vw, 4.85rem);
                line-height: .92;
                font-weight: 1000;
                color: var(--junina-blue);
                text-shadow: 2px 3px 0 rgba(244,185,66,.46);
                margin-top: .12rem;
            }

            .turma-pontos-label {
                margin-top: .42rem;
                font-size: .96rem;
                font-weight: 850;
                color: #72553e;
            }

            .turma-breakdown {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: .65rem;
                margin-top: 1.05rem;
            }

            .mini-score {
                background: rgba(255, 224, 163, .70);
                border: 2px solid rgba(244, 185, 66, .54);
                border-radius: 20px;
                padding: .7rem .45rem;
                box-shadow: 0 8px 18px rgba(79, 52, 28, .08);
            }

            .mini-score span {
                display: block;
                font-size: .78rem;
                font-weight: 950;
                color: #72553e;
                margin-bottom: .25rem;
                text-transform: uppercase;
                letter-spacing: .35px;
            }

            .mini-score strong {
                display: block;
                font-size: 1.52rem;
                line-height: 1;
                font-weight: 1000;
                color: var(--junina-red);
            }

            .provas-score {
                background: rgba(225, 241, 255, .78);
                border-color: rgba(34,87,122,.20);
            }

            .prendas-score {
                background: rgba(255, 231, 173, .74);
                border-color: rgba(244,185,66,.54);
            }

            /* GALERIA */
            .gallery-heading {
                margin-top: 2.05rem;
            }

            div[data-testid="stVerticalBlockBorderWrapper"] {
                background:
                    linear-gradient(145deg, rgba(255,255,255,.88), rgba(255,248,231,.988));
                border: 4px solid rgba(244,185,66,.48) !important;
                border-radius: 26px !important;
                box-shadow: 0 14px 32px rgba(79,52,28,.14);
                overflow: hidden;
                backdrop-filter: blur(1px);
            }

            div[data-testid="stVerticalBlockBorderWrapper"] img,
            div[data-testid="stImage"] img {
                height: auto !important;
                object-fit: contain !important;
                border-radius: 18px;
                background: rgba(255, 248, 231, .85);
            }

            div[data-testid="stImageCaption"] {
                color: #7a5d42;
                font-weight: 950;
                text-align: center;
            }

            .gallery-empty-native {
                min-height: 220px;
                border-radius: 20px;
                background:
                    linear-gradient(145deg, rgba(255,255,255,.82), rgba(255,248,231,.95));
                border: 2px dashed rgba(184,59,46,.28);
                display: grid;
                place-items: center;
                text-align: center;
                color: #7a5d42;
                font-weight: 950;
                padding: 1rem;
            }

            .gallery-empty-icon {
                font-size: 2.8rem;
                line-height: 1;
                margin-bottom: .35rem;
            }

            .gallery-empty-native small {
                display: block;
                margin-top: .25rem;
                font-size: .78rem;
                color: #9a7652;
            }

            .photo-dialog-title {
                text-align: center;
                color: var(--junina-red);
                font-size: 1.35rem;
                font-weight: 1000;
                margin-bottom: .8rem;
            }

            [data-testid="stDialog"] div[role="dialog"] {
                border-radius: 28px;
            }

            [data-testid="stDialog"] div[data-testid="stImage"] img {
                max-height: 78vh;
                width: 100%;
                object-fit: contain !important;
                background: rgba(255,248,231,.92);
                border-radius: 20px;
            }

            /* FOOTER */
            .footer-note {
                text-align: center;
                margin: 1.7rem auto 0;
                color: #7a5d42;
                font-weight: 800;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: .45rem;
                flex-wrap: wrap;
            }

            .footer-note span {
                color: var(--junina-red);
                font-weight: 1000;
            }

            /* RESPONSIVO */
            @media (max-width: 980px) {
                .stApp:after {
                    opacity: .16;
                    background-size: 1150px auto;
                    background-position: center 150px;
                }

                .event-hero {
                    flex-direction: column;
                    align-items: stretch;
                    text-align: center;
                }

                .hero-left {
                    flex-direction: column;
                    text-align: center;
                }

                .hero-tags {
                    justify-content: center;
                }

                .mascot-stage {
                    min-width: auto;
                    min-height: auto;
                }

                .mascotes-img {
                    width: min(280px, 70vw);
                    max-height: 210px;
                }

                .ranking-grid {
                    grid-template-columns: 1fr;
                }

                .turma-card.rank-1,
                .turma-card.rank-1:hover {
                    transform: none;
                }
            }

            @media (max-width: 640px) {
                .block-container {
                    padding-top: .75rem;
                }

                .stApp:after {
                    opacity: .13;
                    background-size: 950px auto;
                    background-position: center 180px;
                }

                .director-band {
                    border-radius: 20px;
                    padding: .72rem .8rem;
                }

                .event-hero {
                    padding: 1rem;
                    border-radius: 26px;
                }

                .brand-logo-frame {
                    width: 108px;
                    height: 108px;
                    flex-basis: 108px;
                    border-radius: 24px;
                }

                .brand-logo {
                    width: 92px;
                    height: 92px;
                }

                .title-wrap h1 {
                    font-size: clamp(2.1rem, 10vw, 3rem);
                    white-space: normal;
                }

                .title-wrap p {
                    font-size: 1rem;
                }

                .hero-tags span {
                    font-size: .78rem;
                }

                .turma-card {
                    min-height: 330px;
                }

                .turma-breakdown {
                    grid-template-columns: 1fr;
                }

                .gallery-empty-native {
                    min-height: 180px;
                }
            }
        </style>
    """

    css = css.replace("%%FUNDO_BACKGROUND_IMAGE%%", fundo_background_rule)

    st.markdown(css, unsafe_allow_html=True)