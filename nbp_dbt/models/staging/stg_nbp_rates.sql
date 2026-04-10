with source as ( 
    select * from {{source('exch_rates', 'raw_exchange_rates')}}
)

select 
    currency,
    code,
    mid,
    effective_date,
    created_at
from source
