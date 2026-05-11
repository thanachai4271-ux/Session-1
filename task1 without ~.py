import pandas as pd

s, c, p = map(pd.read_csv, ['sales_transactions.csv', 'customers.csv', 'products.csv'])
for n, d in zip(['sales', 'customers', 'products'], [s, c, p]): print(f'\n=== {n} ==='); display(d.head())

bd = lambda df, cl: sum((pd.to_datetime(df[x], errors='coerce').pipe(lambda dt: dt.isna() | (dt.dt.year.between(2010,2025) == False))).sum() for x in cl)
bn = lambda df, cl: sum((pd.to_numeric(df[x].astype(str).str.replace('$','',regex=False), errors='coerce')<0).sum() for x in cl if x in df.columns)

k = ['Invalid Dates','Negative Values','Invalid IDs','Unexpected Values','Formatting Issues']
ch = [
    ('sales_transactions.csv', s, [bd(s,['date']), bn(s,['quantity','price','discount_amount']), ((s.customer_id.isin(c.customer_id) == False) | (s.product_id.isin(p.product_id) == False)).sum(), 0, 0]),
    ('customers.csv', c, [bd(c,['join_date','last_purchase_date']), bn(c,['total_spending','average_order_value']), 0, (c.gender.notna() & (c.gender.isin(['M','F']) == False)).sum(), c.email.str.contains('[A-Z]', na=False).sum()]),
    ('products.csv', p, [bd(p,['introduced_date']), bn(p,['price','cost']), 0, (p.category.notna() & (p.category.isin(['Pastries','Bread','Tarte']) == False)).sum(), p[['price','cost']].apply(lambda x: x.astype(str).str.contains(r'\$',na=False)).sum().sum()])
]

open('Session1_DataExploration_short.txt','w',encoding='utf-8').write(f'\n{"-"*30}\n'.join(f"### File: {n}\nData Types:\n" + '\n'.join(f" - {x}: {y}" for x,y in df.dtypes.items()) + "\n\nInconsistencies:\n" + '\n'.join(f" - {x}: {y}" for x,y in zip(k, v)) for n, df, v in ch) + f'\n{"-"*30}\n')
