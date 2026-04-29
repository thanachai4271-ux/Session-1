import pandas as pd; from sklearn.cluster import KMeans; from sklearn.preprocessing import StandardScaler

s = pd.read_csv('sales_transactions_cleaned.csv')
s['r'] = s.quantity * s.price - pd.to_numeric(s.discount_amount, errors='coerce').fillna(0)
f = s.groupby('customer_id').agg(t=('transaction_id','nunique'), r=('r','mean')).reset_index()
f['c'] = KMeans(3, random_state=42, n_init=10).fit_predict(StandardScaler().fit_transform(f[['t','r']])) + 1
s = s.merge(f[['customer_id', 'c']])
tp = s.groupby(['c', 'product_id']).quantity.sum().sort_values(ascending=False).reset_index().groupby('c').product_id.apply(list)
pu = s.groupby('customer_id').product_id.apply(set)

rows = [[cid, cl] + ([p for p in tp[cl] if p not in pu[cid]][:3] + [None]*3)[:3] for cid, cl in zip(f.customer_id, f.c)]
pd.DataFrame(rows, columns=['customer_id', 'cluster_label', 'recommended_product_1', 'recommended_product_2', 'recommended_product_3']).to_csv('Session5_Segmentation_and_Recommendations_shortv2.csv', index=False)
