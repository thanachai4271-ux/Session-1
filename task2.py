import pandas as pd, numpy as np, warnings; warnings.filterwarnings('ignore')

# 1. โหลดข้อมูล
c, s = pd.read_csv('customers.csv'), pd.read_csv('sales_transactions.csv')

# 2. คลีนอายุ, เบอร์โทร, โปรโมชัน (ใช้ Chain Method)
c['age'] = c['age'].fillna(c['age'].median())
c['phone_number'] = c['phone_number'].fillna('0').astype(str).str.replace(r'[^0-9+]', '', regex=True).replace(['', '00'], '0')
s['promotion_id'] = s['promotion_id'].fillna(0)

# 3. จัดการวันที่แบบย่อ (ใช้ Lambda + Pipe + Between)
dt_fix = lambda x: pd.to_datetime(x.fillna('2024-01-01'), errors='coerce', format='mixed').dt.normalize().pipe(
    lambda d: d.where(d.dt.year.between(2000, 2025))
) + pd.to_timedelta(np.random.randint(32400, 61201, len(x)), unit='s')

# เรียกใช้งานรวดเดียวด้วย .apply()
c[['join_date', 'last_purchase_date']] = c[['join_date', 'last_purchase_date']].apply(dt_fix)
s['date'] = dt_fix(s['date'])

# 4. ส่งออกไฟล์ (เขียนให้อยู่บรรทัดเดียวกันด้วย ;)
c.to_csv('customers_cleaned_FINAL.csv', index=False); s.to_csv('sales_transactions_cleaned_FINAL.csv', index=False)
print("✅ สร้างไฟล์ใหม่ (FINAL) พร้อมแก้วันที่เพี้ยนเรียบร้อย!")
