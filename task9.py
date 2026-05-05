import pandas as pd

s = pd.read_csv('sales_transactions_cleaned.csv')

m = pd.to_datetime(s.date).dt.to_period('M').nunique()
c = s.assign(r = s.quantity * s.price - s.discount_amount.fillna(0)).groupby('customer_id', as_index=False)['r'].sum().assign(customer_id=lambda x: x.customer_id.astype(int), cltv=lambda x: (x.r * 36 / m).round(2))[['customer_id', 'cltv']]

c.to_csv('Session1_CLTV_short_short.csv', index=False)
