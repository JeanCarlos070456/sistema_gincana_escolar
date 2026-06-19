# Painel Streamlit — Gincana Festa Junina

Painel web em Streamlit com base Supabase para acompanhar a pontuação acumulada da gincana de Festa Junina.

## Funcionalidades

- Painel sem sidebar.
- 3 cards centralizados: Jardim, Maternal e Acompanhamento Escolar.
- Ranking acumulado com 1º, 2º e 3º lugar.
- Pontuação vinda do Supabase/PostgreSQL.
- Acesso restrito da diretora por senha autenticada no Supabase Auth.
- Lançamento diário de pontos acumulativos.
- Galeria com 4 fotos carregadas do Supabase Storage.
- Atualização das imagens pelo painel da diretora.
- Design com temática de Festa Junina.

## Estrutura

```text
.
├── app.py
├── requirements.txt
├── assets/
│   ├── logo.png
│   └── mascotes.png
├── .streamlit/
│   └── secrets.toml.example
├── supabase/
│   └── schema.sql
└── src/
    ├── core/
    │   ├── database.py
    │   ├── session.py
    │   └── settings.py
    ├── repositories/
    │   ├── galeria_repository.py
    │   ├── pontuacoes_repository.py
    │   └── turmas_repository.py
    ├── services/
    │   ├── auth_service.py
    │   ├── galeria_service.py
    │   ├── pontuacao_service.py
    │   └── ranking_service.py
    └── ui/
        ├── admin_dialog.py
        ├── assets.py
        ├── components.py
        └── styles.py
```

## Como configurar o Supabase

1. Crie um projeto no Supabase.
2. Abra o **SQL Editor**.
3. Execute o arquivo:

```text
supabase/schema.sql
```

Esse script cria:

- `turmas`
- `pontuacoes`
- `galeria_fotos`
- `vw_ranking_turmas`
- bucket público `galeria-junina`

## Criar usuário da diretora

No Supabase:

1. Vá em **Authentication > Users**.
2. Crie um usuário com e-mail da diretora.
3. Defina a senha.
4. Coloque o mesmo e-mail no `DIRECTOR_EMAIL` do `secrets.toml`.

O painel pede apenas a senha, mas autentica no Supabase usando o e-mail salvo em secrets.

## Secrets

Copie:

```text
.streamlit/secrets.toml.example
```

para:

```text
.streamlit/secrets.toml
```

E preencha:

```toml
SUPABASE_URL = "https://SEU-PROJETO.supabase.co"
SUPABASE_ANON_KEY = "SUA-ANON-KEY"
SUPABASE_SERVICE_ROLE_KEY = "SUA-SERVICE-ROLE-KEY"
DIRECTOR_EMAIL = "diretora@suaescola.com.br"
SUPABASE_GALLERY_BUCKET = "galeria-junina"
```

A `SUPABASE_SERVICE_ROLE_KEY` nunca deve ser commitada. Ela fica somente no servidor/Streamlit Cloud Secrets.

## Assets

Coloque estes arquivos na pasta `assets/`:

```text
assets/logo.png
assets/mascotes.png
```

Se eles não existirem, o sistema mostra placeholders e continua funcionando.

## Rodar localmente

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

No Linux/Mac:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Fluxo de uso

1. O público visualiza o placar e a galeria.
2. A diretora clica em **Acesso Diretor**.
3. Digita a senha.
4. Lança os pontos do dia para as turmas.
5. Opcionalmente atualiza as 4 imagens da galeria.
6. O sistema salva novos lançamentos acumulativos e atualiza o ranking.

## Observação técnica

A pontuação não sobrescreve o total. Cada atualização cria um lançamento diário em `pontuacoes`. O total exibido vem da soma desses lançamentos via `vw_ranking_turmas`. Isso preserva histórico e permite auditoria posterior.
