import pandas as pd, matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages

df = pd.read_csv('sales_transactions_cleaned.csv')
m = df.assign(date=pd.to_datetime(df['date']).dt.strftime('%Y-%m'), r=(df.quantity * df.price) - df.discount_amount.fillna(0)).groupby('date').agg(r=('r','sum'),t=('transaction_id','nunique')).assign(a=lambda x: x.r/x.t).reset_index()
t3 = m.nlargest(3,'r')[['date','r']].assign(r=lambda x:  x.r.apply('${:,.2f}'.format))

with PdfPages('sale.pdf') as pdf:
	f,ax = plt.subplots(4,1,figsize=(10,16)); f.subplots_adjust(hspace=0.4)
	
	spec = zip(['r','t','a'],['blue','green','red'],['Total Revenue','Transaction','Average Order Value'])
	for  a,c,cl,t in zip(ax[:3], *zip(*spec)):
		a.plot(m.date,m[c],color=cl,marker='o'); a.set_title(t,weight='bold'); a.tick_params('x',rotation=45); a.grid(ls='--')
		
	ax[3].axis('off'); ax[3].set_title('Top 3 Months', weight='bold', y=0.9); ax[3].table(cellText=t3.values, colLabels=['Month','Total Revenue'], cellLoc='center', bbox=[0, 0.2, 1, 0.6])
	
	pdf.savefig(f,bbox_inches='tight'); plt.close()
