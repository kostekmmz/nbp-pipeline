SELECT month, avg_monthly, code,
LAG(avg_monthly, 1 ) over (
PARTITION BY code
ORDER BY month
) previous_month_avg
,(1-(avg_monthly/LAG(avg_monthly, 1 ) over (
PARTITION BY code
ORDER BY month
)))*100 as "mom_change_pct"
from {{ref('mart_monthly_avg')}}

