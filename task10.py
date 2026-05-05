import pandas as pd

c, l = pd.read_csv('customers_cleaned.csv'), pd.read_csv('Session1_CLTV.csv')

c['k'] = c.churned.astype(str).str.lower().str.strip().isin({'true','yes','1','y'})
cr = round(c.k.mean() * 100, 2)

a = l.merge(c).groupby('k')['cltv'].mean().round(2)

pd.DataFrame([{'churn_rate': cr, 'avg_cltv_churned': a.get(True, 0.0), 'avg_cltv_active': a.get(False, 0.0)}]).to_csv('Session1_Churn_Analysis_short.csv', index=False)
