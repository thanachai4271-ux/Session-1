import pandas as pd,matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages

s,p = pd.read_csv('sales_transactions_cleaned.csv'), pd.read_csv('products.csv')
p['cost'],p['category'] = pd.to_numeric(p.cost.astype(str).str.strip('$'),errors='coerce'), p.category.replace({'Pastry' : 'Pastries'})
m = s.assign(r=s.quantity * s.price - s.discount_amount.fillna(0)).merge(p[['product_id','product_name','category','cost']],on='product_id',how='left')
t3 = m.groupby('product_name')[['quantity','r']].sum().nlargest(3,'quantity').reset_index().assign(r=lambda x:  x.r.apply('${:,.2f}'.format)).set_axis(['Product Name','Total Quantity Sold','Total Revenue'],axis=1)

with PdfPages('per.pdf') as pdf:
	f,ax = plt.subplots(figsize=(10,5))
	
	m[m.category.isin(['Pastries','Bread','Tarte'])].groupby('category')['r'].sum().plot.bar(color=['lightpink','lightgreen','lightblue'],ax=ax,title='Total Revenue by Category',ylabel='Total Revenue',xlabel='Category',rot=0); ax.tick_params('x',rotation=45); ax.grid(axis='y',ls='--')
	pdf.savefig(f,bbox_inches='tight'); plt.close()
	
	f,ax = plt.subplots(figsize=(7,4))

	ax.axis('off'); ax.set_title('Top 3 Best Selling Products',weight='bold',y=0.85); ax.table(cellText=t3.values,colLabels=t3.columns,loc='center',cellLoc='center').scale(1,2)
	pdf.savefig(f,bbox_inches='tight'); plt.close()
