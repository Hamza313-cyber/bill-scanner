-- Bill Scanner: Supabase SQL Editor mein ye poora chalaiye (ek baar)

create table if not exists public.purchases (
  id          bigint generated always as identity primary key,
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  created_at  timestamptz not null default now(),
  supplier    text,
  bill_no     text,
  bill_date   text,
  product     text not null,
  batch       text,
  expiry      text,
  qty         numeric,
  free_qty    numeric,
  mrp         numeric,
  rate        numeric,
  gst_percent numeric,
  amount      numeric,
  bill_total  numeric
);

create index if not exists purchases_user_idx on public.purchases (user_id, created_at desc);

-- Har user sirf apna data dekh/likh/mita sake
alter table public.purchases enable row level security;

drop policy if exists "own rows select" on public.purchases;
drop policy if exists "own rows insert" on public.purchases;
drop policy if exists "own rows delete" on public.purchases;

create policy "own rows select" on public.purchases for select using (auth.uid() = user_id);
create policy "own rows insert" on public.purchases for insert with check (auth.uid() = user_id);
create policy "own rows delete" on public.purchases for delete using (auth.uid() = user_id);
