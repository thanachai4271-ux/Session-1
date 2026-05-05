import pandas as pd, numpy as np
s, p = pd.read_csv('sales_transactions_cleaned.csv'), pd.read_csv('products.csv')

s['r'] = s.quantity * s.price - s.discount_amount.fillna(0)
p['c'] = pd.to_numeric(p.cost.astype(str).str.replace(r'[^0-9+]', '', regex=1), 'coerce')

f = s.groupby('product_id', as_index=0).agg(total_quantity_sold=('quantity','sum'), total_revenue=('r','sum')).merge(p[['product_id','c']])
f['profit_margin'] = (1 - f.total_quantity_sold * f.c / f.total_revenue).round(4)
f.drop(columns='c').sort_values('total_revenue', ascending=0).round(2).to_csv('Session5_Product_Performance_short_short.csv', index=0)

g = s.assign(m=pd.to_datetime(s.date).dt.strftime('%Y-%m')).groupby(['product_id','m']).agg(q=('quantity','sum'), v=('price','mean')).groupby('product_id')
d = (g.q.pct_change() / g.v.pct_change()).replace([np.inf, -np.inf], np.nan).groupby('product_id').mean().round(4).reset_index(name='e')
d['suggested_price_change'] = d.e.map(lambda x: '-5%' if abs(x)>1 else ('+5%' if x==x else '0%'))
d.rename(columns={'e':'price_elasticity_of_demand'}).to_csv('Session5_Price_Analysis_short.csv', index=0)
