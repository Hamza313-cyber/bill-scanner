-- Bill Scanner: SALES support. Supabase > SQL Editor mein ye ek baar chalaiye.
-- Purani saari entries apne aap "purchase" maani jayengi.
alter table public.purchases
  add column if not exists kind text not null default 'purchase';

alter table public.purchases drop constraint if exists purchases_kind_check;
alter table public.purchases add constraint purchases_kind_check check (kind in ('purchase','sale'));
