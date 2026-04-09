import pandas as pd, matplotlib.pyplot as plt, matplotlib.ticker as mt
from matplotlib.backends.backend_pdf import PdfPages

# ── 1. โหลด & เตรียมข้อมูล ──────────────────────────────────────────────────
d = pd.read_csv('sales_transactions_cleaned.csv')
N = lambda c: pd.to_numeric(d[c].astype(str).str.replace('$', '', regex=False), errors='coerce').fillna(0)
m = d.assign(date=pd.to_datetime(d['date']).dt.strftime('%Y-%m'), r=d.quantity * N('price') - N('discount_amount')).groupby('date').agg(r=('r','sum'), t=('transaction_id','nunique')).assign(a=lambda x: x.r/x.t).reset_index()

t3 = m.nlargest(3,'r')[['date','r']].assign(r=lambda x: x.r.apply("${:,.0f}".format))
plt.rcParams.update({'font.family':'DejaVu Sans', 'axes.spines.top':False, 'axes.spines.right':False})

# ── 2. สร้าง PDF (รวมกราฟและตารางในหน้าเดียว) ──────────────────────────────────
with PdfPages('Session1_SalesTrendsv8.pdf') as pdf:
    # แบ่งกระดาษเป็น 4 แถว (3 แถวแรกเป็นกราฟ, แถวสุดท้ายเป็นตาราง)
    f, ax = plt.subplots(4, 1, figsize=(10, 14), facecolor='white', gridspec_kw={'height_ratios': [1, 1, 1, 0.7]})
    f.subplots_adjust(hspace=0.65) # เพิ่มช่องไฟระหว่างแถว
    f.suptitle('Sales Trends Dashboard', fontsize=15, fontweight='bold', y=0.94)

    # --- ส่วนที่ 1: วาดกราฟเส้นลงใน ax 3 ตัวแรก (ax[:3]) ---
    specs = zip(['r','t','a'], ['royalblue','forestgreen','crimson'], 
                ['Total Revenue','Transactions','Avg Order Value (AOV)'],
                [lambda v,_: f'${v/1e3:.0f}K', lambda v,_: f'{v:,.0f}', lambda v,_: f'${v:,.0f}'])

    for a, c, cl, t, fm in zip(ax[:3], *zip(*specs)):
        a.plot(m.date, m[c], color=cl, lw=2.2, marker='o', ms=4.5, mfc='white', mew=1.8, zorder=3)
        a.fill_between(m.date, m[c], alpha=0.12, color=cl)
        a.set_facecolor('whitesmoke'); a.set_title(t, fontweight='bold', pad=8)
        a.grid(axis='y', color='lightgray', zorder=0); a.tick_params('both', labelsize=8, colors='darkslategray')
        a.tick_params('x', rotation=45); a.yaxis.set_major_formatter(mt.FuncFormatter(fm))
        
    # --- ส่วนที่ 2: สร้างตารางลงใน ax ตัวสุดท้าย (ax[3]) ---
    ax[3].axis('off')
    ax[3].set_title('🏆 Top 3 Revenue Months', fontsize=12, fontweight='bold', pad=10)
    
    tb = ax[3].table(cellText=t3.values, colLabels=['Month','Total Revenue'], loc='center', cellLoc='center')
    tb.auto_set_font_size(False); tb.set_fontsize(10); tb.scale(0.8, 2) # ปรับ scale ความกว้างตารางให้สวยงาม

    for (r, c), cl in tb.get_celld().items():
        cl.set_edgecolor('lightgray')
        cl.set_facecolor('darkblue' if r==0 else 'aliceblue' if r%2==0 else 'white')
        if r==0: cl.set_text_props(color='white', weight='bold')

    # สั่งเซฟแค่รอบเดียว (รวมทั้งหน้า)
    pdf.savefig(f, bbox_inches='tight')
    plt.close()

print("✅ PDF สร้างเรียบร้อย (รวมกราฟและตารางไว้ในหน้าเดียวแล้ว)!")
