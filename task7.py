import pandas as pd; from sklearn.cluster import KMeans; from sklearn.preprocessing import StandardScaler

s = pd.read_csv('sales_transactions_cleaned.csv')
f = s.assign(r=s.quantity*s.price-s.discount_amount.fillna(0)).groupby('customer_id').agg(t=('transaction_id','nunique'), r=('r','mean')).reset_index()
f['c'] = KMeans(3, n_init=10, random_state=42).fit_predict(StandardScaler().fit_transform(f[['t','r']])) + 1

tp = s.merge(f[['customer_id','c']]).groupby(['c','product_id']).quantity.sum().sort_values(ascending=0).reset_index().groupby('c').product_id.agg(list)
pu = s.groupby('customer_id').product_id.agg(set)

pd.DataFrame([[u, c] + ([p for p in tp[c] if p not in pu[u]][:3] + [None]*3)[:3] for u, c in zip(f.customer_id, f.c)], columns=['customer_id','cluster_label'] + [f'recommended_product_{i}' for i in (1,2,3)]).to_csv('Session5_Segmentation_and_Recommendations_shortv3.csv', index=False)
