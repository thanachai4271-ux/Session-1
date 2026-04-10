import pandas as pd, matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages
s, p = pd.read_csv('sales_transactions_cleaned.csv'), pd.read_csv('products.csv')

p['cost'], p['category'] = pd.to_numeric(p.cost.astype(str).str.strip('$'), errors='coerce'), p.category.replace('Pastry', 'Pastries')
m = s.assign(rev=s.quantity*s.price-s.discount_amount.fillna(0)).merge(p[['product_id','product_name','category','cost']], on='product_id', how='left')
t3 = m.groupby('product_name')[['quantity','rev']].sum().nlargest(3,'quantity').reset_index().assign(rev=lambda x: x.rev.apply('${:,.2f}'.format)).set_axis(['product_name','Total Quantity Sold','Total Revenue'], axis=1)

with PdfPages('Session1_ProductPerformancev2.pdf') as d:
      f, a = plt.subplots(2, 1, figsize=(8, 10)); f.subplots_adjust(hspace=0.4)
      m[m.category.isin(['Pastries','Bread','Tarte'])].groupby('category')['rev'].sum().plot.bar(color=['lightpink','lightblue','lightgreen'], ax=a[0], title='Total Revenue by Category', ylabel='Total Revenue ($)', rot=0); a[0].set_axisbelow(True); a[0].tick_params('x',rotation=45); a[0].grid(ls='--')
      a[1].axis('off'); a[1].set_title('Top 3 Best-Selling Products', weight='bold',y=0.85); a[1].table(cellText=t3.values, colLabels=t3.columns, cellLoc='center',bbox=[0,0.2,1,0.6])
      d.savefig(f, bbox_inches='tight'); plt.close()
