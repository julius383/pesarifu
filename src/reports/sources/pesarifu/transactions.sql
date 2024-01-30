select
    transaction_reference,
    initiated_at,
    amount,
    ta.account_name,
    original_detail,
    owner_account_id
from transaction t
inner join transactional_account ta
on t.participant_account_id = ta.id
order by initiated_at
