import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')
s, p = pd.read_csv('sales_transactions_cleaned.csv'), pd.read_csv('products.csv')

i, q, r, c, e = 'product_id', 'total_quantity_sold', 'total_revenue', 'cost_clean', 'price_elasticity_of_demand'

s['revenue'] = s.quantity * s.price - pd.to_numeric(s.discount_amount, 'coerce').fillna(0)
s['M'] = pd.to_datetime(s.date).dt.strftime('%Y-%m')
p[c] = pd.to_numeric(p.cost.astype(str).str.replace(r'[^\d.-]', '', regex=1), 'coerce').abs()

f = s.groupby(i, as_index=0).agg(**{q:('quantity','sum'), r:('revenue','sum')}).merge(p[[i,c]], how='left')
f['profit_margin'] = ((f[r] - f[q]*f[c]) / f[r]).round(4)
f[[i,q,r,'profit_margin']].sort_values(r, ascending=0).round(2).to_csv('Session5_Product_Performance_short_short.csv', index=0)

g = s.groupby([i,'M']).agg(Q=('quantity','sum'), P=('price','mean')).groupby(i)
d = (g.Q.pct_change() / g.P.pct_change()).replace([np.inf,-np.inf], np.nan).groupby(i).mean().reset_index(name=e).round(4)
d['suggested_price_change'] = d[e].map(lambda v: '-5%' if abs(v)>1 else('+5%' if v==v else '0%'))
d.to_csv('Session5_Price_Analysis_short.csv', index=0)
