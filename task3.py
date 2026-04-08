import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.gridspec import GridSpec

# ── โหลด & เตรียมข้อมูล ──────────────────────────────────────────────────────
df = pd.read_csv('sales_transactions_cleaned.csv')
df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m')
df['revenue'] = (
    df['quantity'] *
    pd.to_numeric(df['price'].astype(str).str.replace('$', ''), errors='coerce')
) - pd.to_numeric(df['discount_amount'], errors='coerce').fillna(0)

# ── Monthly Metrics ───────────────────────────────────────────────────────────
m = (df.groupby('date')
       .agg(rev=('revenue','sum'), tx=('transaction_id','nunique'))
       .assign(aov=lambda x: x['rev']/x['tx'])
       .sort_index().reset_index())

top3 = (m.nlargest(3,'rev')[['date','rev']]
         .assign(rev=lambda x: x['rev'].apply(lambda v: f"${v:,.0f}")))

# ── Style Helpers ─────────────────────────────────────────────────────────────
# เปลี่ยน Hex เป็นชื่อสีทั้งหมด
PALETTE   = ['royalblue', 'forestgreen', 'crimson'] 
BG, GRID  = 'whitesmoke', 'lightgray'
plt.rcParams.update({'font.family':'DejaVu Sans', 'axes.spines.top':False,
                     'axes.spines.right':False})

def style_ax(ax, title, color, y_fmt=None):
    ax.set_facecolor(BG)
    ax.set_title(title, fontsize=11, fontweight='bold', color='black', pad=8)
    ax.grid(axis='y', color=GRID, linewidth=0.8, zorder=0)
    ax.tick_params(axis='x', rotation=45, labelsize=7.5, colors='darkslategray')
    ax.tick_params(axis='y', labelsize=7.5, colors='darkslategray')
    if y_fmt: ax.yaxis.set_major_formatter(mticker.FuncFormatter(y_fmt))
    # gradient fill under line
    ys = ax.lines[0].get_ydata()
    ax.fill_between(ax.lines[0].get_xdata(), ys, alpha=0.12, color=color)

# ── Page 1 : 3 Line Charts ────────────────────────────────────────────────────
with PdfPages('Session1_SalesTrendsv7.pdf') as pdf:
    fig = plt.figure(figsize=(10,11), facecolor='white')
    fig.suptitle('Sales Trends Dashboard', fontsize=14, fontweight='bold',
                 color='black', y=0.97)
    gs = GridSpec(3, 1, figure=fig, hspace=0.55)

    specs = [
        ('rev', PALETTE[0], 'Total Revenue',        lambda v,_: f'${v/1e3:.0f}K'),
        ('tx',  PALETTE[1], 'Transactions',          lambda v,_: f'{v:,.0f}'),
        ('aov', PALETTE[2], 'Avg Order Value (AOV)', lambda v,_: f'${v:,.0f}'),
    ]

    for i,(col,color,title,fmt) in enumerate(specs):
        ax = fig.add_subplot(gs[i])
        ax.plot(m['date'], m[col], color=color, lw=2.2,
                marker='o', ms=4.5, markerfacecolor='white',
                markeredgewidth=1.8, zorder=3)
        style_ax(ax, title, color, fmt)

    pdf.savefig(fig, bbox_inches='tight')
    plt.close()

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
