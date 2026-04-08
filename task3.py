import pandas as pd, matplotlib.pyplot as plt, matplotlib.ticker as mt
from matplotlib.backends.backend_pdf import PdfPages

# ── 1. โหลด & เตรียมข้อมูล (ยุบรวมไว้ใน Chain เดียว) ──────────────────────────
d = pd.read_csv('sales_transactions_cleaned.csv')
N = lambda c: pd.to_numeric(d[c].astype(str).str.replace('$', '', regex=False), errors='coerce').fillna(0)
m = d.assign(date=pd.to_datetime(d['date']).dt.strftime('%Y-%m'), r=d.quantity * N('price') - N('discount_amount')) \
     .groupby('date').agg(r=('r','sum'), t=('transaction_id','nunique')).assign(a=lambda x: x.r/x.t).reset_index()

t3 = m.nlargest(3,'r')[['date','r']].assign(r=lambda x: x.r.apply("${:,.0f}".format))
plt.rcParams.update({'font.family':'DejaVu Sans', 'axes.spines.top':False, 'axes.spines.right':False})

# ── 2. สร้าง PDF ─────────────────────────────────────────────────────────────
with PdfPages('Session1_SalesTrendsv7.pdf') as pdf:
    # --- หน้า 1 : กราฟเส้น (ใช้ zip รวบ Loop) ---
    f, ax = plt.subplots(3, 1, figsize=(10, 11), facecolor='white'); f.subplots_adjust(hspace=0.55)
    f.suptitle('Sales Trends Dashboard', fontsize=14, fontweight='bold', y=0.97)

    specs = zip(['r','t','a'], ['royalblue','forestgreen','crimson'], 
                ['Total Revenue','Transactions','Avg Order Value (AOV)'],
                [lambda v,_: f'${v/1e3:.0f}K', lambda v,_: f'{v:,.0f}', lambda v,_: f'${v:,.0f}'])

    for a, c, cl, t, fm in zip(ax, *zip(*specs)):
        a.plot(m.date, m[c], color=cl, lw=2.2, marker='o', ms=4.5, mfc='white', mew=1.8, zorder=3)
        a.fill_between(m.date, m[c], alpha=0.12, color=cl)
        a.set_facecolor('whitesmoke'); a.set_title(t, fontweight='bold', pad=8)
        a.grid(axis='y', color='lightgray', zorder=0); a.tick_params('both', labelsize=7.5, colors='darkslategray')
        a.tick_params('x', rotation=45); a.yaxis.set_major_formatter(mt.FuncFormatter(fm))
        
    pdf.savefig(f, bbox_inches='tight'); plt.close()

    # --- หน้า 2 : ตาราง (ย่อคำสั่งลงสีแบบบรรทัดเดียว) ---
    f, a = plt.subplots(figsize=(6, 2.2), facecolor='white'); a.axis('off')
    a.set_title('Top 3 Revenue Months', fontsize=12, fontweight='bold', pad=10)
    
    tb = a.table(cellText=t3.values, colLabels=['Month','Total Revenue'], loc='center', cellLoc='center')
    tb.auto_set_font_size(False); tb.set_fontsize(10); tb.scale(1, 2.2)

    for (r, c), cl in tb.get_celld().items():
        cl.set_edgecolor('lightgray')
        cl.set_facecolor('darkblue' if r==0 else 'aliceblue' if r%2==0 else 'white') # รวบ If-Else
        if r==0: cl.set_text_props(color='white', weight='bold')

    pdf.savefig(f, bbox_inches='tight'); plt.close()

print("✅ PDF สร้างเรียบร้อย (เวอร์ชันย่อสุดๆ)!")

    # ── Page 2 : Top-3 Table ──────────────────────────────────────────────────
    fig, ax = plt.subplots(figsize=(6, 2.2), facecolor='white')
    ax.axis('off')
    ax.set_title('Top 3 Revenue Months', fontsize=12, fontweight='bold',
                 color='black', pad=10)

    tbl = ax.table(cellText=top3.values,
                   colLabels=['Month','Total Revenue'],
                   loc='center', cellLoc='center')
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    tbl.scale(1, 2.2)

    for (r,c), cell in tbl.get_celld().items():
        cell.set_edgecolor('lightgray') # เปลี่ยนขอบเป็นสี lightgray
        if r == 0:
            cell.set_facecolor('darkblue') # หัวตารางสีน้ำเงินเข้ม
            cell.set_text_props(color='white', fontweight='bold')
        elif r % 2 == 0:
            cell.set_facecolor('aliceblue') # แถวคู่สีฟ้าอ่อน
        else:
            cell.set_facecolor('white')

    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

print("✅ PDF สร้างเรียบร้อย พร้อมใช้ชื่อสีภาษาอังกฤษ!")
