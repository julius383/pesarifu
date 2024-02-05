-- build struct in accounts.sql with account information
SELECT
    ua.id as user_id,
    ta.id as account_id,
    account_name,
    type,
    ua.uuid as user_uuid
FROM transactional_account ta
INNER JOIN user_account ua on holder_id = ua.id
WHERE holder_id IS NOT NULL;
