```sql distinct_months
select
    distinct date_trunc('month', initiated_at)
from ${user_transactions}
```

<Dropdown name=relevant_period defaultValue={ distinct_months.length > 2 ? "month" : "week" } >
    <DropdownOption value="month" valueLabel="Monthly"/>
    <DropdownOption value="week" valueLabel="Weekly" />
</Dropdown>


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


<ECharts config={
{
  title: {
    top: 30,
    left: 'center',
    text: 'Daily Transaction Activity'
  },
  tooltip: {
    trigger: 'item',
    formatter: function(params) {
        var val = currencyFormat(params.value[1], "kes");
        return val;
    },
  },
  visualMap: {
    min: 0,
    max: Math.pow(10, (heatmap_stats[0].amount_max).toString().length),
    type: 'piecewise',
    orient: 'horizontal',
    left: 'center',
    top: 65
  },
  calendar: {
    top: 120,
    left: 30,
    right: 30,
    cellSize: ['auto', 13],
    range: stats[0].range_end > stats[0].end_date ? [stats[0].range_start, stats[0].range_end] : [stats[0].start_date, stats[0].end_date],
    itemStyle: {
      borderWidth: 0.5
    },
    yearLabel: { show: false }
  },
  series: {
    type: 'heatmap',
    coordinateSystem: 'calendar',
    data: heatmap_data.map(item => [item.name, item.value])
  }
}
}
/>
