```sql distinct_months
select
    distinct date_trunc('month', initiated_at)
from ${user_transactions}
```


```sql period_trunced
select
    date_trunc('${inputs.relevant_period}', initiated_at) as period,
    sum(abs(credit)) as credit_sum,
    sum(abs(credit)) * 100 / (select sum(abs(credit)) from ${user_transactions}) as credit_percent,
    sum(abs(debit)) as debit_sum,
    sum(abs(debit)) * 100 / (select sum(abs(debit)) from ${user_transactions}) as debit_percent
from ${user_transactions}
group by period
order by period
```

```sql period_trunced_credit_min
select *
from ${period_trunced}
where
    credit_sum = (select min(credit_sum) from ${period_trunced})
```
```sql period_trunced_debit_min
select *
from ${period_trunced}
where
    debit_sum = (select min(debit_sum) from ${period_trunced})
```
```sql period_trunced_credit_max
select *
from ${period_trunced}
where
    credit_sum = (select max(credit_sum) from ${period_trunced})
```
```sql period_trunced_debit_max
select *
from ${period_trunced}
where
    debit_sum = (select max(debit_sum) from ${period_trunced})
```

{#if inputs.relevant_period == "month"}

For the transactions beginning _{fmt(period_trunced[0].period, 'longdate')}_
, it is evident that _{fmt(period_trunced_credit_max[0].period, "mmmm, yyyy")}_ observed
the highest activity, with a total amount of **{fmt(period_trunced_credit_max[0].credit_sum, "kes0k")}** accounting
for **{fmt(period_trunced_credit_max[0].credit_percent, "num2")}%** of outflow transactions. Conversely,
_{fmt(period_trunced_credit_min[0].period, "mmmm, yyyy")}_ experienced the lowest volume of activity,
reflecting **{fmt(period_trunced_credit_min[0].credit_sum, "kes0k")}** constituting
**{fmt(period_trunced_credit_min[0].credit_percent, "num2")}%** of the overall.


For the same period the highest inflow activity was observed in _{fmt(period_trunced_debit_max[0].period, "mmmm, yyyy")}_,
with a total amount of **{fmt(period_trunced_debit_max[0].debit_sum, "kes0k")}**
accounting for **{fmt(period_trunced_debit_max[0].debit_percent, "num2")}%** of
inlfow transactions. Contrarily _{fmt(period_trunced_debit_min[0].period, "mmmm, yyyy")}_ experienced the lowest
volume of activity reflecting **{fmt(period_trunced_debit_min[0].debit_sum, "kes0k")}** composing
**{fmt(period_trunced_debit_min[0].debit_percent, "num2")}%** of the total.

{:else}

For the transactions beginning _{fmt(period_trunced[0].period, 'longdate')}_
, it is evident that the week starting _{fmt(period_trunced_credit_max[0].period, "longdate")}_ observed
the highest activity, with a total amount of **{fmt(period_trunced_credit_max[0].credit_sum, "kes0k")}** accounting
for **{fmt(period_trunced_credit_max[0].credit_percent, "num2")}%** of outflow transactions. Conversely, the week of
_{fmt(period_trunced_credit_min[0].period, "longdate")}_ experienced the lowest volume of activity,
reflecting **{fmt(period_trunced_credit_min[0].credit_sum, "kes0k")}** constituting
**{fmt(period_trunced_credit_min[0].credit_percent, "num2")}%** of the overall.


For the same period the highest inflow activity was observed in the week of _{fmt(period_trunced_debit_max[0].period, "longdate")}_,
with a total amount of **{fmt(period_trunced_debit_max[0].debit_sum, "kes0k")}**
accounting for **{fmt(period_trunced_debit_max[0].debit_percent, "num2")}%** of all
inlfow transactions. Contrarily the week of _{fmt(period_trunced_debit_min[0].period, "longdate")}_ experienced the lowest
volume of activity reflecting **{fmt(period_trunced_debit_min[0].debit_sum, "kes0k")}** composing
**{fmt(period_trunced_debit_min[0].debit_percent, "num2")}%** of the total.

{/if}


```sql barchart_data
with cte as (
    select
        credit_sum as 'credits',
        debit_sum as 'debits',
        period
    from ${period_trunced}
)
unpivot cte
ON credits, debits
into
    name 'type'
    value amount

```

<Dropdown name=relevant_period defaultValue={ distinct_months.length > 2 ? "month" : "week" } >
    <DropdownOption value="month" valueLabel="Monthly"/>
    <DropdownOption value="week" valueLabel="Weekly" />
</Dropdown>


<BarChart
    data={barchart_data}
    x=period
    y=amount
    series=type
    yFmt="kes"
    title={`Total Cashflow by ${inputs.relevant_period} in KSh`}
    labels=true
    labelFmt=num0k
    colorPalette={
        [
        '#de0000',
        '#228b22',
        ]
    }
/>


```sql cashflow_day_grouped
select
    sum(abs(amount)) as day_value,
    cast(date_trunc('day', initiated_at) as date)::date as trunced_date
from ${user_transactions}
group by trunced_date
```

```sql heatmap_data
select
    trunced_date as name,
    day_value as value
from ${cashflow_day_grouped}
```

```sql heatmap_stats
select max(value) as amount_max
from ${heatmap_data}
```

<CalendarHeatmap
  data={heatmap_data}
  date=name
  value=value
  valueFmt="kes0k"
  title='Daily Transaction Activity'
  subtitle='Total transaction value for each day'
/>
