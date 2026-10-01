-- =====================================================================
-- Bill Scanner: SAARE NAYE UPDATES (sales, billing, QR codes, stock count)
-- Supabase > SQL Editor > New query > ye poora paste karke Run dabaiye.
-- Ek se zyada baar chalane par bhi koi nuksaan nahi (safe to re-run).
-- =====================================================================

-- 1) Sales + billing: purchase/sale ka farq aur discount
alter table public.purchases
  add column if not exists kind text not null default 'purchase',
  add column if not exists discount numeric;

alter table public.purchases drop constraint if exists purchases_kind_check;
alter table public.purchases add constraint purchases_kind_check check (kind in ('purchase','sale'));

-- 2) Barcode / QR code ko product se jodna (ek baar link, hamesha yaad)
create table if not exists public.product_codes (
  id         bigint generated always as identity primary key,
  user_id    uuid not null default auth.uid() references auth.users(id) on delete cascade,
  created_at timestamptz not null default now(),
  code       text not null,
  product    text not null,
  batch      text,
  unique (user_id, code)
);
alter table public.product_codes enable row level security;
drop policy if exists "codes select" on public.product_codes;
drop policy if exists "codes insert" on public.product_codes;
drop policy if exists "codes update" on public.product_codes;
drop policy if exists "codes delete" on public.product_codes;
create policy "codes select" on public.product_codes for select using (auth.uid() = user_id);
create policy "codes insert" on public.product_codes for insert with check (auth.uid() = user_id);
create policy "codes update" on public.product_codes for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "codes delete" on public.product_codes for delete using (auth.uid() = user_id);

-- 3) Stock ginti (count) ki report: system vs asli, kami kitni
create table if not exists public.stock_counts (
  id          bigint generated always as identity primary key,
  user_id     uuid not null default auth.uid() references auth.users(id) on delete cascade,
  created_at  timestamptz not null default now(),
  session_id  text,
  product     text not null,
  batch       text,
  system_qty  numeric,
  counted_qty numeric,
  diff        numeric,
  value_diff  numeric
);
create index if not exists stock_counts_user_idx on public.stock_counts (user_id, created_at desc);
alter table public.stock_counts enable row level security;
drop policy if exists "counts select" on public.stock_counts;
drop policy if exists "counts insert" on public.stock_counts;
drop policy if exists "counts delete" on public.stock_counts;
create policy "counts select" on public.stock_counts for select using (auth.uid() = user_id);
create policy "counts insert" on public.stock_counts for insert with check (auth.uid() = user_id);
create policy "counts delete" on public.stock_counts for delete using (auth.uid() = user_id);
