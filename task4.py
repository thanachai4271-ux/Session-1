import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.backends.backend_pdf import PdfPages

# ── โหลด & เตรียมข้อมูล ──────────────────────────────────────────────────────
s = pd.read_csv('sales_transactions_cleaned.csv')
p = pd.read_csv('products.csv')

p['cost'] = pd.to_numeric(p['cost'].astype(str).str.replace('$','',regex=False), errors='coerce')
p['category'] = p['category'].replace({'Pastry':'Pastries'})

m = (s.assign(revenue=(s['quantity']*s['price']) - s['discount_amount'].fillna(0))
      .merge(p[['product_id','product_name','category','cost']], on='product_id', how='left'))

# ── Metrics ───────────────────────────────────────────────────────────────────
CATS = ['Pastries','Bread','Tarte']
cr = m[m['category'].isin(CATS)].groupby('category')['revenue'].sum().reindex(CATS)

t3 = (m.groupby('product_name')[['quantity','revenue']].sum()
       .nlargest(3,'quantity').reset_index()
       .rename(columns={'product_name':'Product','quantity':'Qty Sold','revenue':'Revenue'})
       .assign(Revenue=lambda x: x['Revenue'].apply(lambda v: f"${v:,.0f}")))

# ── Style ─────────────────────────────────────────────────────────────────────
plt.rcParams.update({'font.family':'DejaVu Sans','axes.spines.top':False,'axes.spines.right':False})
# เปลี่ยนจาก Hex Code เป็นชื่อสีภาษาอังกฤษ
PALETTE = ['lightcoral', 'cornflowerblue', 'mediumaquamarine'] 
BG, GRID = 'whitesmoke', 'lightgray'

# ── Page 1 : Bar Chart ────────────────────────────────────────────────────────
with PdfPages('Session1_ProductPerformancev2.pdf') as pdf:
    fig, ax = plt.subplots(figsize=(7, 4.5), facecolor='white')
    bars = ax.bar(cr.index, cr.values, color=PALETTE, width=0.5, zorder=3)

    ax.set_facecolor(BG)
    ax.set_title('Total Revenue by Category', fontsize=13, fontweight='bold', color='black', pad=12)
    ax.set_ylabel('Total Revenue ($)', fontsize=9, color='darkslategray')
    ax.tick_params(colors='darkslategray')
    ax.grid(axis='y', color=GRID, linewidth=0.8, zorder=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f'${v/1e3:.0f}K'))

    for bar in bars:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+bar.get_height()*0.01,
                f'${bar.get_height():,.0f}', ha='center', va='bottom', fontsize=8.5,
                fontweight='bold', color='black')

    pdf.savefig(fig, bbox_inches='tight'); plt.close()

    # ── Page 2 : Table ────────────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(7, 2.5), facecolor='white')
    ax.axis('off')
    ax.set_title('Top 3 Best-Selling Products', fontsize=12, fontweight='bold',
                 color='black', pad=10)

    tbl = ax.table(cellText=t3.values, colLabels=t3.columns, loc='center', cellLoc='center')
    tbl.auto_set_font_size(False); tbl.set_fontsize(10); tbl.scale(1, 2.2)

    for (r,c), cell in tbl.get_celld().items():
        cell.set_edgecolor('lightgray') # ขอบตาราง
        if r == 0:
            cell.set_facecolor('darkblue') # หัวตาราง
            cell.set_text_props(color='white', fontweight='bold')
        else:
            cell.set_facecolor('aliceblue' if r%2==0 else 'white') # สลับสีแถวตาราง

    pdf.savefig(fig, bbox_inches='tight'); plt.close()

print("✅ Session1_ProductPerformancev2.pdf สร้างเรียบร้อย (เวอร์ชันใช้ชื่อสี)!")
