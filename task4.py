import pandas as pd, matplotlib.pyplot as plt, matplotlib.ticker as mt
from matplotlib.backends.backend_pdf import PdfPages

# ── 1. โหลด & เตรียมข้อมูล ──────────────────────────────────────────────────
s, p = pd.read_csv('sales_transactions_cleaned.csv'), pd.read_csv('products.csv')
p['category'] = p['category'].replace({'Pastry':'Pastries'})
m = s.assign(rev=s.quantity * s.price - s.discount_amount.fillna(0)).merge(p, on='product_id', how='left')

cr = m[m.category.isin(['Pastries','Bread','Tarte'])].groupby('category')['rev'].sum().reindex(['Pastries','Bread','Tarte'])
t3 = m.groupby('product_name')[['quantity','rev']].sum().nlargest(3,'quantity').reset_index() \
      .rename(columns={'product_name':'Product','quantity':'Qty Sold','rev':'Revenue'}) \
      .assign(Revenue=lambda x: x.Revenue.apply("${:,.0f}".format))

plt.rcParams.update({'font.family':'DejaVu Sans', 'axes.spines.top':False, 'axes.spines.right':False})

# ── 2. สร้าง PDF (หน้าเดียว) ───────────────────────────────────────────────
with PdfPages('Session1_ProductPerformancev5.pdf') as pdf:
    f, ax = plt.subplots(2, 1, figsize=(7, 7.5), facecolor='white', gridspec_kw={'height_ratios': [1.5, 1]})
    f.subplots_adjust(hspace=0.35) # ปรับช่องไฟเพิ่มนิดนึง เพื่อเว้นที่ให้แกน X

    # --- ส่วนที่ 1: กราฟแท่ง (ด้านบน) ---
    b = ax[0].bar(cr.index, cr.values, color=['lightcoral','cornflowerblue','mediumaquamarine'], width=0.5, zorder=3)
    
    # 👉 เพิ่ม xlabel='Category' ตรงบรรทัดนี้ครับ
    ax[0].set(facecolor='whitesmoke', xlabel='Category', ylabel='Total Revenue ($)')
    ax[0].set_title('Total Revenue by Category', weight='bold', pad=12)
    
    ax[0].tick_params(colors='darkslategray'); ax[0].grid(axis='y', color='lightgray', zorder=0)
    ax[0].yaxis.set_major_formatter(mt.FuncFormatter(lambda v,_: f'${v/1e3:.0f}K'))
    
    [ax[0].text(i.get_x()+0.25, i.get_height()*1.02, f'${i.get_height():,.0f}', ha='center', weight='bold') for i in b]

    # --- ส่วนที่ 2: ตาราง (ด้านล่าง) ---
    ax[1].axis('off'); ax[1].set_title('🏆 Top 3 Best-Selling Products', weight='bold', pad=10)
    tb = ax[1].table(cellText=t3.values, colLabels=t3.columns, loc='center', cellLoc='center')
    tb.auto_set_font_size(False); tb.set_fontsize(10); tb.scale(1, 2.2)

    for (r, c), cl in tb.get_celld().items():
        cl.set_edgecolor('lightgray')
        cl.set_facecolor('darkblue' if r==0 else 'aliceblue' if r%2==0 else 'white')
        if r==0: cl.set_text_props(color='white', weight='bold')

    pdf.savefig(f, bbox_inches='tight')
    plt.close()

print("✅ เพิ่มชื่อแกน x เป็น Category เรียบร้อย!")
