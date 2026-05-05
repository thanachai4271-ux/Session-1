import pandas as pd

v = {f: pd.read_csv(f) for f in ['sales_transactions.csv', 'products.csv', 'customers.csv']}
r = ""
for n, d in v.items():
    S, T, N, c = lambda x: d[x].astype(str).str, ['True','False','Nan'], [0]*len(d), n[0]
    r += f"### File: {n}\n\n{d.head().to_string()}\n\nData Types:\n" + "\n".join(f"- {k}: {t}" for k, t in d.dtypes.items()) + f"\n\n{'--'*30}\n\n"
open('Session1_DataExploration.txt', 'w', encoding='utf-8').write(r.strip()); display(d.head())
