# Users

```sql users
select
    user_uuid,
    '/' || user_uuid as user_link,
from pesarifu.accounts
group by 1
```

<DataTable
    data={users}
    link=user_link
/>
