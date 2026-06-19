-- =========================================================
-- Sistema: Painel Gincana Festa Junina
-- Banco: Supabase/PostgreSQL
-- Execute este arquivo no SQL Editor do Supabase.
-- =========================================================

create extension if not exists pgcrypto;

-- -----------------------------
-- Tabela fixa das turmas
-- -----------------------------
create table if not exists public.turmas (
    id uuid primary key default gen_random_uuid(),
    slug text not null unique,
    nome text not null,
    ordem integer not null default 0,
    ativa boolean not null default true,
    criado_em timestamptz not null default now()
);

insert into public.turmas (slug, nome, ordem)
values
    ('jardim', 'Jardim', 1),
    ('maternal', 'Maternal', 2),
    ('acompanhamento-escolar', 'Acompanhamento Escolar', 3)
on conflict (slug) do update
set nome = excluded.nome,
    ordem = excluded.ordem,
    ativa = true;

-- -----------------------------
-- Lançamentos diários de pontos
-- Cada inserção soma no placar geral.
-- -----------------------------
create table if not exists public.pontuacoes (
    id uuid primary key default gen_random_uuid(),
    turma_id uuid not null references public.turmas(id) on delete restrict,
    pontos integer not null check (pontos >= 0),
    data_lancamento date not null default current_date,
    observacao text,
    criado_por_email text,
    criado_em timestamptz not null default now()
);

create index if not exists idx_pontuacoes_turma_id on public.pontuacoes(turma_id);
create index if not exists idx_pontuacoes_data_lancamento on public.pontuacoes(data_lancamento desc);

-- -----------------------------
-- Fotos da galeria
-- O campo slot limita a galeria em 4 posições fixas.
-- -----------------------------
create table if not exists public.galeria_fotos (
    id uuid primary key default gen_random_uuid(),
    slot integer not null unique check (slot between 1 and 4),
    titulo text,
    storage_path text not null,
    public_url text not null,
    mime_type text,
    atualizado_por_email text,
    atualizado_em timestamptz not null default now()
);

create index if not exists idx_galeria_fotos_slot on public.galeria_fotos(slot);

-- -----------------------------
-- View de ranking acumulado
-- -----------------------------
create or replace view public.vw_ranking_turmas as
select
    t.id,
    t.slug,
    t.nome,
    t.ordem,
    coalesce(sum(p.pontos), 0)::integer as pontos_total,
    dense_rank() over (
        order by coalesce(sum(p.pontos), 0) desc, t.ordem asc
    ) as posicao
from public.turmas t
left join public.pontuacoes p on p.turma_id = t.id
where t.ativa = true
group by t.id, t.slug, t.nome, t.ordem
order by pontos_total desc, t.ordem asc;

-- -----------------------------
-- Bucket público para a galeria
-- Observação: o app usa service_role no servidor para upload.
-- Nunca exponha service_role no navegador ou em repositório público.
-- -----------------------------
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values (
    'galeria-junina',
    'galeria-junina',
    true,
    5242880,
    array['image/png', 'image/jpeg', 'image/webp']
)
on conflict (id) do update
set public = true,
    file_size_limit = 5242880,
    allowed_mime_types = array['image/png', 'image/jpeg', 'image/webp'];
