select 
code,
round(avg(mid),4) as avg_monthly,
date_trunc('month', effective_date)::DATE as month
from {{ref('stg_nbp_rates')}}
group by date_trunc('month', effective_date), code
