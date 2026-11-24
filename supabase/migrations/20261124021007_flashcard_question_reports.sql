create table public.flashcard_question_reports (
  user_id uuid not null references auth.users (id) on delete cascade,
  card_id text not null check (char_length(card_id) between 1 and 120),
  reported boolean not null,
  updated_at bigint not null check (updated_at between 0 and 9007199254740991),
  primary key (user_id, card_id)
);

alter table public.flashcard_question_reports enable row level security;
revoke all on public.flashcard_question_reports from public, anon, authenticated;
grant select, insert, update on public.flashcard_question_reports to authenticated;

create policy "Read own question reports" on public.flashcard_question_reports for select to authenticated
  using (user_id = (select auth.uid()));
create policy "Insert own question reports" on public.flashcard_question_reports for insert to authenticated
  with check (user_id = (select auth.uid()));
create policy "Update own question reports" on public.flashcard_question_reports for update to authenticated
  using (user_id = (select auth.uid()))
  with check (user_id = (select auth.uid()));

create function public.sync_flashcard_question_reports(account_id uuid, records jsonb)
returns table (card_id text, reported boolean, updated_at bigint)
language plpgsql
security invoker
set search_path = ''
as $$
declare
  owner_id uuid := (select auth.uid());
begin
  if owner_id is null or owner_id is distinct from account_id then
    raise exception 'Reports belong to another account' using errcode = '42501';
  end if;

  insert into public.flashcard_question_reports as stored (user_id, card_id, reported, updated_at)
  select owner_id, incoming.card_id, incoming.reported, incoming.updated_at
  from jsonb_to_recordset(records) as incoming (card_id text, reported boolean, updated_at bigint)
  order by incoming.card_id
  on conflict on constraint flashcard_question_reports_pkey do update
    set reported = excluded.reported, updated_at = excluded.updated_at
    where excluded.updated_at > stored.updated_at;

  return query
    select stored.card_id, stored.reported, stored.updated_at
    from public.flashcard_question_reports as stored
    where stored.user_id = owner_id;
end;
$$;

revoke execute on function public.sync_flashcard_question_reports(uuid, jsonb) from public, anon;
grant execute on function public.sync_flashcard_question_reports(uuid, jsonb) to authenticated;
