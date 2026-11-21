-- Daily study totals for the progress charts. Each browser uploads its own days under a
-- device id, so totals from a phone and a laptop add up without double counting.
create table public.flashcard_activity (
  user_id uuid not null references auth.users (id) on delete cascade,
  device_id text not null check (device_id ~ '^[A-Za-z0-9-]{8,64}$'),
  day date not null,
  reviews integer not null check (reviews between 0 and 100000),
  correct integer not null check (correct between 0 and 100000),
  red integer not null check (red between 0 and 100000),
  amber integer not null check (amber between 0 and 100000),
  green integer not null check (green between 0 and 100000),
  updated_at bigint not null check (updated_at between 0 and 9007199254740991),
  primary key (user_id, device_id, day),
  check (correct <= reviews)
);

alter table public.flashcard_activity enable row level security;
revoke all on public.flashcard_activity from anon, authenticated;
grant select, insert, update on public.flashcard_activity to authenticated;

create policy "Read own activity" on public.flashcard_activity for select to authenticated
  using (user_id = (select auth.uid()));

create policy "Insert own activity" on public.flashcard_activity for insert to authenticated
  with check (user_id = (select auth.uid()));

create policy "Update own activity" on public.flashcard_activity for update to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

create function public.sync_flashcard_activity(account_id uuid, device text, records jsonb)
returns table (device_id text, day date, reviews integer, correct integer, red integer, amber integer, green integer, updated_at bigint)
language plpgsql
security invoker
set search_path = ''
as $$
declare
  owner_id uuid := (select auth.uid());
begin
  if owner_id is null or owner_id is distinct from account_id then
    raise exception 'Activity belongs to another account' using errcode = '42501';
  end if;

  insert into public.flashcard_activity as stored (user_id, device_id, day, reviews, correct, red, amber, green, updated_at)
  select owner_id, device, incoming.day, incoming.reviews, incoming.correct, incoming.red, incoming.amber, incoming.green, incoming.updated_at
  from jsonb_to_recordset(records) as incoming (day date, reviews integer, correct integer, red integer, amber integer, green integer, updated_at bigint)
  order by incoming.day
  on conflict on constraint flashcard_activity_pkey do update
    set reviews = excluded.reviews,
        correct = excluded.correct,
        red = excluded.red,
        amber = excluded.amber,
        green = excluded.green,
        updated_at = excluded.updated_at
    where excluded.updated_at > stored.updated_at;

  return query
    select stored.device_id, stored.day, stored.reviews, stored.correct, stored.red, stored.amber, stored.green, stored.updated_at
    from public.flashcard_activity as stored
    where stored.user_id = owner_id and stored.day >= current_date - 400;
end;
$$;

revoke execute on function public.sync_flashcard_activity(uuid, text, jsonb) from public, anon;
grant execute on function public.sync_flashcard_activity(uuid, text, jsonb) to authenticated;
