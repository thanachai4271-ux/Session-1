import pandas as pd, matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages
s, p = pd.read_csv('sales_transactions_cleaned.csv'), pd.read_csv('products.csv')

p['cost'], p['category'] = pd.to_numeric(p.cost.astype(str).str.strip('$'), errors='coerce'), p.category.replace('Pastry', 'Pastries')
m = s.assign(rev=s.quantity*s.price-s.discount_amount.fillna(0)).merge(p[['product_id','product_name','category','cost']], on='product_id', how='left')
t3 = m.groupby('product_name')[['quantity','rev']].sum().nlargest(3,'quantity').reset_index().assign(rev=lambda x: x.rev.map('${:,.2f}'.format)).set_axis(['product_name','Total Quantity Sold','Total Revenue'], axis=1)

with PdfPages('Session1_ProductPerformancev2.pdf') as d:
      f, a = plt.subplots(); m[m.category.isin(['Pastries','Bread','Tarte'])].groupby('category')['rev'].sum().plot.bar(color=['#ff9999','#66b3ff','#99ff99'], ax=a, title='Total Revenue by Category', ylabel='Total Revenue ($)', rot=0); d.savefig(f, bbox_inches='tight'); plt.close()
      f, a = plt.subplots(figsize=(9,3)); a.axis('off'); a.set_title('Top 3 Best-Selling Products', weight='bold'); a.table(cellText=t3.values, colLabels=t3.columns, loc='center', cellLoc='center').scale(1,2)
      pdf.savefig(f, bbox_inches='tight'); plt.close()
