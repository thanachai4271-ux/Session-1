import pandas as pd, numpy as np

c, s = pd.read_csv('customers.csv'), pd.read_csv('sales_transactions.csv')

c['age'] = c['age'].fillna(c['age'].median())
c['phone_number'] = c['phone_number'].fillna('0').astype(str).str.replace(r'[^0-9+]', '', regex=True).replace(['', '00'], '0')
s['promotion_id'] = s['promotion_id'].fillna(0)

fix = lambda x: pd.to_datetime(x, errors='coerce', format='mixed').pipe(lambda d: d.where(d.dt.year.between(2000, 2025))).fillna(pd.Timestamp('2024-01-01')).dt.normalize() + pd.to_timedelta(np.random.randint(9*3600, 17*3600+1, len(x)), unit='s')

c[['join_date', 'last_purchase_date']] = c[['join_date', 'last_purchase_date']].apply(fix)
s['date'] = fix(s['date'])

c.to_csv('customers_cleaned.csv', index=False); s.to_csv('sales_transactions_cleaned.csv', index=False)
