import pandas as pd, matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages

d = pd.read_csv('sales_transactions_cleaned.csv')
m = (d.assign(date=pd.to_datetime(d['date']).dt.strftime('%Y-%m'), r=(d.quantity * d.price) - d.discount_amount.fillna(0)).groupby('date').agg(r=('r','sum'), t=('transaction_id','nunique')).assign(a=lambda x: x.r/x.t).reset_index())
t3 = m.nlargest(3, 'r')[['date','r']].assign(r=lambda x: x.r.apply("${:,.2f}".format))

with PdfPages('Session1_SalesTrendsv2.pdf') as pdf:
    f, ax = plt.subplots(4, 1, figsize=(10, 13))
    f.subplots_adjust(hspace=0.9)
      
    specs = zip(['r','t','a'], ['blue','green','red'], ['Total Revenue','Transactions','Average Order Value'])
    for a, c, cl, t in zip(ax[:3], *zip(*specs)):
        a.plot(m.date, m[c], marker='o', color=cl); a.set_title(t, weight='bold'); a.tick_params('x', rotation=45); a.grid(ls='--')
          
    ax[3].axis('off'); ax[3].set_title('Top 3 Months', weight='bold', pad=20); ax[3].table(cellText=t3.values, colLabels=['Month', 'Total Revenue'], loc='center', cellLoc='center').scale(1, 2)
    pdf.savefig(f, bbox_inches='tight'); plt.close() 
