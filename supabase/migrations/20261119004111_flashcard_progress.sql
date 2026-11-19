create table public.flashcard_progress (
  user_id uuid not null references auth.users (id) on delete cascade,
  card_id text not null check (char_length(card_id) between 1 and 120),
  rating text not null check (rating in ('known', 'review')),
  streak smallint not null check (streak between 0 and 6),
  rated_at bigint not null check (rated_at between 0 and 9007199254740991),
  due_at bigint not null check (due_at between rated_at and 9007199254740991),
  primary key (user_id, card_id)
);

alter table public.flashcard_progress enable row level security;
revoke all on public.flashcard_progress from anon, authenticated;
grant select, insert, update on public.flashcard_progress to authenticated;

create policy "Read own progress" on public.flashcard_progress for select to authenticated
  using (user_id = (select auth.uid()));

create policy "Insert own progress" on public.flashcard_progress for insert to authenticated
  with check (user_id = (select auth.uid()));

create policy "Update own progress" on public.flashcard_progress for update to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

create function public.sync_flashcard_progress(account_id uuid, records jsonb)
returns table (card_id text, rating text, streak smallint, rated_at bigint, due_at bigint)
language plpgsql
security invoker
set search_path = ''
as $$
declare
  owner_id uuid := (select auth.uid());
begin
  if owner_id is null or owner_id is distinct from account_id then
    raise exception 'Progress belongs to another account' using errcode = '42501';
  end if;

  insert into public.flashcard_progress as stored (user_id, card_id, rating, streak, rated_at, due_at)
  select owner_id, incoming.card_id, incoming.rating, incoming.streak, incoming.rated_at, incoming.due_at
  from jsonb_to_recordset(records) as incoming (card_id text, rating text, streak smallint, rated_at bigint, due_at bigint)
  order by incoming.card_id
  on conflict on constraint flashcard_progress_pkey do update
    set rating = excluded.rating,
        streak = excluded.streak,
        rated_at = excluded.rated_at,
        due_at = excluded.due_at
    where excluded.rated_at > stored.rated_at;

  return query
    select stored.card_id, stored.rating, stored.streak, stored.rated_at, stored.due_at
    from public.flashcard_progress as stored
    where stored.user_id = owner_id;
end;
$$;

revoke execute on function public.sync_flashcard_progress(uuid, jsonb) from public, anon;
grant execute on function public.sync_flashcard_progress(uuid, jsonb) to authenticated;
