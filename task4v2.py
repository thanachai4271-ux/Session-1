import pandas as pd,matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages; from matplotlib.ticker import StrMethodFormatter

s,p = pd.read_csv('sales_transactions_cleaned.csv'), pd.read_csv('products.csv')
p['category'] = p.category.replace({'Pastry' : 'Pastries'})
m = s.assign(r=s.quantity * s.price - s.discount_amount.fillna(0)).merge(p,on='product_id',how='left')
t3 = m.groupby('product_name')[['quantity','r']].sum().nlargest(3,'quantity').reset_index().assign(r=lambda x:  x.r.apply('${:,.2f}'.format)).set_axis(['Product Name','Total Quantity Sold','Total Revenue'],axis=1)

with PdfPages('Session1_ProductPerformancev2.pdf') as pdf:
	f,ax = plt.subplots(figsize=(10,5))
	m[m.category.isin(['Pastries','Bread','Tarte'])].groupby('category')['r'].sum().plot.bar(color=['r','g','b'],ax=ax,title='Total Revenue by Category',ylabel='Total Revenue',xlabel='Category',rot=0); ax.tick_params('x',rotation=45); ax.grid(axis='y',ls='--'); ax.yaxis.set_major_formatter(StrMethodFormatter('${x:,.0f}'))
	pdf.savefig(f,bbox_inches='tight'); plt.close()
	
	f,ax = plt.subplots(figsize=(6,2))
	ax.axis('off'); ax.set_title('Top 3 Best Selling Products',weight='bold'); ax.table(cellText=t3.values,colLabels=t3.columns,loc='center',cellLoc='center').scale(1,2)
	pdf.savefig(f,bbox_inches='tight'); plt.close()
