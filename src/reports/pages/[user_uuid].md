---
title: Financial Report by Pesarifu
---
``` sql user_accounts
select * from accounts where user_uuid = UUID'${params.user_uuid}' limit 1
```

``` sql account_ids
select account_id from ${user_accounts}
```

``` sql user_transactions
select
    transaction_reference,
    cast(to_timestamp(initiated_at::bigint) as timestamp) as initiated_at,
    amount,
    case when amount < 0 then amount else 0 end as credit,
    case when amount > 0 then amount else 0 end as debit,
    account_name,
    original_detail
from transactions where owner_account_id in ${account_ids}
```

```sql stats
SELECT
    COUNT(1) AS num_transactions,
    AVG(debit) AS avg_debit,
    AVG(abs(credit)) AS avg_credit,
    AVG(abs(amount)) AS avg_value,
    MIN(initiated_at) AS start_date,
    start_date - interval '1 month' as range_start,
    start_date + interval '1 month' as range_end,
    MAX(initiated_at) AS end_date,
    date_trunc('month', MIN(initiated_at)) AS start_month,
    MAX(abs(amount)) AS max_amount,
    MIN(abs(amount)) AS min_amount,
    SUM(abs(amount)) AS sum_amount,
    SUM(debit) as sum_debit,
    SUM(ABS(credit)) as sum_credit
FROM ${user_transactions}
```

<script>
function currencyFormat(data) {
  data = parseFloat(data);
  return data.toLocaleString('en-KE', {
    style: 'currency',
    currency: 'KES'
  });
}

function accountString(account) {
    let res;
    switch (account.type) {
        case "mobile_money_account":
            res = "Mobile Account"
            break;
        case "safaricom_buygoods_account":
            res = "BuyGoods Account"
            break;
        case "safaricom_paybill_account":
            res = "PayBill Account"
            break;
        case "bank_account":
            res = "Bank Account"
            break;
        default:
            res = "Account"
            break;
    }
    return `Analysis for ${res}: ${account.account_name}`;
}
</script>


## {accountString(user_accounts[0])}


There were **<Value data={stats} column=num_transactions />** transactions in the period
between _<Value data={stats} column=start_date fmt="mmmm d, yyyy" />_ and _<Value data={stats} column=end_date fmt="mmmm d, yyyy"/>_


```sql day_grouped
select
    avg(amount) as avg_amount,
    sum(debit) as cash_in,
    sum(credit) as cash_out,
    date_trunc('day', initiated_at) as trunced_date
from ${user_transactions}
group by trunced_date
```
<LineChart
    data={day_grouped}
    x='trunced_date'
    y={["cash_out", "cash_in"]}
    title="Cashflow"
    yAxisTitle="Transaction Amount"
    xAxisTitle="Date"
    yFmt="kes"
    colorPalette={
        [
        '#de0000',
        '#228b22',
        ]
    }
>
    <ReferenceLine y={stats[0].avg_value} label="Average Transaction Value"/>
</LineChart>


### Transaction Patterns Over Time

{@partial "period-comparison.md"}


### Account Activity Examination

{@partial "account-comparison.md"}

<div class="print:hidden">

<DataTable data={user_transactions} search="true" rows=20>
    <Column id="initiated_at" title="Transaction Time" fmt="mmmm d, yyyy H:MM:SS AM/PM"/>
    <Column id="amount" title="Amount in Kshs." fmt="num2"/>
    <Column id="account_name" />
</DataTable>

</div>
