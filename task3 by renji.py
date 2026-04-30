import pandas as pd,matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages

s = pd.read_csv('sales_transactions_cleaned.csv')
mstat = s.assign(date=pd.to_datetime(s['date']).dt.strftime('%Y-%m'),rev=s.quantity*s.price-s.discount_amount.fillna(0)).groupby('date').agg(rev=('rev','sum'),tx=('transaction_id','nunique')).assign(aov=lambda x:x.rev/x.tx).reset_index()
t3 = mstat.nlargest(3,'rev')[['date','rev']].assign(rev=lambda x:x.rev.apply('{:,.2f}'.format))

with PdfPages('S-1.pdf') as pdf:
    axes = mstat.set_index('date')[['rev','tx','aov']].plot(subplots=True,marker='o',figsize=(10,10),grid=True,title=['Total Revenue','Transactions','Average Order Value'],color=['violet','steelblue','seagreen'])
    pdf.savefig(plt.gcf(), bbox_inches='tight'); plt.close()

    fig,ax = plt.subplots(figsize=(6,2)); ax.axis('off')
    ax.set_title('Top 3 month')
    ax.table(cellText=t3.values,colLabels=['Date','Revenue'],loc='center').scale(1,2)
    pdf.savefig(fig,bbox_inches='tight'); plt.close()
