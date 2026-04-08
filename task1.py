import pandas as pd, warnings; warnings.filterwarnings('ignore')

dfs = {f: pd.read_csv(f) for f in ['sales_transactions.csv', 'products.csv', 'customers.csv']}
[(d.head()) for d in dfs.values()] 

r = "" 
for n, d in dfs.items():
    r += f"### File: {n}\nData Types:\n" + "\n".join(f"- {c}: {t}" for c, t in d.dtypes.items()) + "\n\nInconsistencies:\n"
    
    # ตัวช่วยย่อโค้ด: S = ฟังก์ชันแปลงคอลัมน์เป็นข้อความ, TF = ลิสต์ค่า True/False
    S, TF = lambda x: d[x].astype(str).str, ['True','False','Nan']
    
    # 1. Dates (ใช้ != True ดักทั้งค่าว่าง NaT และปีที่ผิดในบรรทัดเดียว)
    dc = d.columns[d.columns.str.contains('(?i)date')]
    dm = pd.concat([pd.to_datetime(d[c], errors='coerce').dt.year.between(2010,2025) != True for c in dc], axis=1).any(axis=1) if len(dc) else [0]*len(d)
    
    # 2. Negatives (ใช้ .intersection หาคอลัมน์ที่ตรงกันแบบสั้นๆ)
    nc = d.columns.intersection(['quantity','price','cost'])
    nm = pd.concat([pd.to_numeric(S(c).replace('\$','',regex=True), errors='coerce') < 0 for c in nc], axis=1).any(axis=1) if len(nc) else [0]*len(d)
    
    # 3. Invalid IDs (เช็คแค่ถ้าชื่อไฟล์ขึ้นต้นด้วยตัว 's' = sales)
    im = (~d.customer_id.isin(dfs['customers.csv'].customer_id) | ~d.product_id.isin(dfs['products.csv'].product_id)) if n[0]=='s' else [0]*len(d)
    
    # 4-5. Unexpected (um) & Format Issues (fm) - ใช้ if-else แบบรวบยอดโดยเช็คจากอักษรตัวแรกของชื่อไฟล์ (c=customers, p=products, s=sales)
    um = (~d.gender.isin(['M','F',pd.NA]) | ~S('membership_status').title().isin(['Basic','Silver','Gold','Nan']) | ~S('churned').title().isin(TF)) if n[0]=='c' else \
         (~d.category.isin(['Pastries','Bread','Tarte','Viennoiserie','Pastry',pd.NA]) | ~S('seasonal').title().isin(TF) | ~S('active').title().isin(TF)) if n[0]=='p' else \
         (~d.payment_method.isin(['Credit Card','Mobile Pay','Cash',pd.NA]) | ~d.channel.isin(['Online','In-store',pd.NA]))
         
    fm = (S('first_name').contains(r'^\s|\s$') | S('email').contains('[A-Z]') | S('phone_number').contains(r'[a-zA-Z\^<|>@]')) if n[0]=='c' else \
         (S('price').contains(r'\$') | S('cost').contains(r'\$')) if n[0]=='p' else [0]*len(d)
         
    # สรุปผล
    r += f"- Invalid Dates: {sum(dm)}\n- Neg Values: {sum(nm)}\n- Invalid IDs: {sum(im)}\n- Unexpected: {sum(um)}\n- Format Issues: {sum(fm)}\n{'-'*30}\n\n"

open('Session1_DataExploration.txt', 'w', encoding='utf-8').write(r.strip())
print("✅ Done!\n" + r.strip())
