import pandas as pd
v = {f: pd.read_csv(f) for f in ['sales_transactions.csv', 'products.csv', 'customers.csv']}
r = ""
for n, d in v.items():
    S, T, N, c = lambda x: d[x].astype(str).str, ['True','False','Nan'], [0]*len(d), n[0]
    r += f"### File: {n}\nData Types:\n" + "\n".join(f"- {k}: {t}" for k, t in d.dtypes.items()) + "\n\nInconsistencies:\n"
    
    dc = [x for x in d if 'date' in x.lower()]
    dm = pd.concat([pd.to_datetime(d[x], errors='coerce').dt.year.between(2010,2025)!=True for x in dc], axis=1).any(axis=1) if dc else N
    nc = [x for x in d if x in ['quantity','price','cost']]
    nm = pd.concat([pd.to_numeric(S(x).replace('\$','',regex=True), errors='coerce')<0 for x in nc], axis=1).any(axis=1) if nc else N
    im = (~d.customer_id.isin(v['customers.csv'].customer_id) | ~d.product_id.isin(v['products.csv'].product_id)) if c=='s' else N
    um = (~d.gender.isin(['M','F',pd.NA]) | ~S('membership_status').title().isin(['Basic','Silver','Gold','Nan']) | ~S('churned').title().isin(T)) if c=='c' else (~d.category.isin(['Pastries','Bread','Tarte','Viennoiserie','Pastry',pd.NA]) | ~S('seasonal').title().isin(T) | ~S('active').title().isin(T)) if c=='p' else (~d.payment_method.isin(['Credit Card','Mobile Pay','Cash',pd.NA]) | ~d.channel.isin(['Online','In-store',pd.NA]))
    fm = (S('first_name').contains(r'^\s|\s$') | S('email').contains('[A-Z]') | S('phone_number').contains(r'[a-zA-Z\^<|>@]')) if c=='c' else (S('price').contains(r'\$') | S('cost').contains(r'\$')) if c=='p' else N
        
    r += f"- Invalid Dates: {sum(dm)}\n- Neg Values: {sum(nm)}\n- Invalid IDs: {sum(im)}\n- Unexpected: {sum(um)}\n- Format Issues: {sum(fm)}\n{'-'*30}\n\n"
open('Session1_DataExploration.txt', 'w', encoding='utf-8').write(r.strip())
