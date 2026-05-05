import pandas as pd, matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages; from matplotlib.ticker import StrMethodFormatter

d = pd.read_csv('sales_transactions_cleaned.csv')
m = (d.assign(date=pd.to_datetime(d['date']).dt.strftime('%Y-%m'), r=(d.quantity * d.price) - d.discount_amount.fillna(0)).groupby('date').agg(r=('r','sum'), t=('transaction_id','nunique')).assign(a=lambda x: x.r/x.t).reset_index())
t3 = m.nlargest(3, 'r')[['date','r']].assign(r=lambda x: x.r.apply("${:,.2f}".format))
data = [('r','tomato','Total Sales Revenue ($)'),('t','steelblue','Number of Transactions'),('a','seagreen','Average Order Value ($)')]

with PdfPages('Session1_SalesTrends.pdf') as pdf:
    for c, cl, t in data:
        f, ax = plt.subplots(figsize=(10, 5)) 
        ax.plot(m.date, m[c], marker='o', color=cl,); ax.set_xlabel('Month'); ax.set_title(t, weight='bold'); ax.tick_params('x', rotation=45); ax.grid(axis='y', ls='--')
        if c in ['r', 'a']:
            ax.yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
        pdf.savefig(f, bbox_inches='tight'); plt.close() 

    f, ax_table = plt.subplots(figsize=(6, 2))
    ax_table.axis('off'); ax_table.set_title('Top 3 Months', weight='bold', pad=20); ax_table.table(cellText=t3.values, colLabels=['Month', 'Total Revenue'], loc='center', cellLoc='center').scale(1, 2)
    pdf.savefig(f, bbox_inches='tight'); plt.close()
