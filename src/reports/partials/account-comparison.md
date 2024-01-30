```sql credits
select
    sum(abs(credit)) as sum_credit,
    sum(abs(credit)) * 100 / (select sum(abs(credit)) from ${user_transactions}) as credit_percent,
    account_name,
    count(*) as transaction_count,
    'credit' as type
from ${user_transactions}
where abs(credit) > 0
group by account_name
order by sum_credit desc
```

Notably, the account _{credits[0].account_name}_ recorded the highest credit
activity, totaling **{fmt(credits[0].sum_credit, "kes0k")}** and constituting
**{fmt(credits[0].credit_percent, "num2")}%** of all credit transactions.

```sql account_grouped
select
    sum(abs(credit)) as sum_credit,
    sum(abs(debit)) as sum_debit,
    account_name
from ${user_transactions}
group by account_name
```

```sql pie_data
select sum_credit as value, account_name as name
from ${account_grouped}
order by value desc
limit 5
```


<ECharts config={
{
  title: {
    top: 30,
    left: 'center',
    text: 'Top 5 Highest Credits by Account'
  },
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
        var val = currencyFormat(params.value);
        return val;
    },
  },
  series: [
    {
      name: 'Paid To',
      type: 'pie',
      radius: '50%',
      data: data.pie_data ,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
}
}
/>


```sql debits
select
    sum(abs(debit)) as sum_debit,
    sum(abs(debit)) * 100 / (select sum(abs(debit)) from ${user_transactions}) as debit_percent,
    account_name,
    count(*) as transaction_count,
    'debit' as type
from ${user_transactions}
where debit > 0
group by account_name
order by sum_debit desc
```

Similarly, the account _{debits[0].account_name}_ recorded the highest debit
activity, totaling **{fmt(debits[0].sum_debit, "kes0k")}** and constituting
**{fmt(debits[0].debit_percent, "num2")}%** of all debit transactions.


```sql pie_data_2
select sum_debit as value, account_name as name
from ${account_grouped}
order by value desc
limit 5
```
<ECharts config={
{
  title: {
    top: 30,
    left: 'center',
    text: 'Top 5 Highest Debits by Account'
  },
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
        var val = currencyFormat(params.value);
        return val;
    },
  },
  series: [
    {
      name: 'Received From',
      type: 'pie',
      radius: '50%',
      data: data.pie_data_2 ,
      emphasis: {
        itemStyle: {
          shadowBlur: 10,
          shadowOffsetX: 0,
          shadowColor: 'rgba(0, 0, 0, 0.5)'
        }
      }
    }
  ]
}
}
/>

```sql aggregated_amounts
(select * from ${debits} limit 25)
union all
(select * from ${credits} limit 25)
```

```sql bubble_data
select
    sum_debit as sum_amount,
    debit_percent as amount_percent,
    account_name,
    transaction_count,
    type
from ${aggregated_amounts}
order by type, transaction_count desc
```

For the top 25 recurrent debit and credit transactions:

- The account _{bubble_data[0].account_name}_ leads in credits with
  **{bubble_data[0].transaction_count}** transactions and a total value
  of **{fmt(bubble_data[0].sum_amount, "kes0k")}**.
- The account _{bubble_data[25].account_name}_ leads in debits with
  **{bubble_data[25].transaction_count}** transactions and a total value
  of **{fmt(bubble_data[25].sum_amount, "kes0k")}**.


<BubbleChart
    data={bubble_data}
    x=amount_percent
    y=sum_amount
    series=type
    title="Top 25 Recurring Debits and Credits by Account"
    size=transaction_count
    xAxisTitle=true
    yAxisTitle=true
    tooltipTitle=account_name
    colorPalette={
        [
        '#228b22',
        '#de0000',
        ]
    }
/>
