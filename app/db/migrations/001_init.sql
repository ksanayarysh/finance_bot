create table if not exists users (
  id bigserial primary key,
  tg_user_id bigint not null unique,
  created_at timestamptz not null default now(),
  currency text not null default 'BRL',
  tz text not null default 'America/Sao_Paulo'
);

create table if not exists categories (
  id bigserial primary key,
  user_id bigint not null references users(id) on delete cascade,
  name text not null,
  kind text not null check (kind in ('expense','income')),
  created_at timestamptz not null default now(),
  unique (user_id, kind, name)
);

create table if not exists transactions (
  id bigserial primary key,
  user_id bigint not null references users(id) on delete cascade,
  kind text not null check (kind in ('expense','income')),
  category_id bigint references categories(id) on delete set null,
  amount numeric(12,2) not null check (amount >= 0),
  note text,
  happened_at date not null,
  created_at timestamptz not null default now()
);

create index if not exists idx_tx_user_date on transactions(user_id, happened_at);
create index if not exists idx_tx_user_kind_date on transactions(user_id, kind, happened_at);
