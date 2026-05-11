import pandas as pd, matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages

c = pd.read_csv('customers_cleaned.csv')
c['membership_status'] = c['membership_status'].str.title()

with PdfPages('Session1_CustomerAnalysis_short.pdf') as pdf:
    ax = pd.cut(c['age'], [17,24,34,44,200], labels=['18-24','25-34','35-44','45+']).value_counts().sort_index().plot.bar(title='Distribution of Customer Age Groups',ylabel='Number of Customers', rot=0); ax.grid(axis='y',ls='--')
    pdf.savefig(plt.gcf(), bbox_inches='tight'); plt.close()
    
    g = c[c['gender'].isin(['M','F'])]['gender'].value_counts(normalize=True).mul(100).map('{:.2f}%'.format).reset_index()
    t = c[c['membership_status'].isin(['Basic','Silver','Gold'])].groupby('membership_status')['total_spending'].mean().map('${:,.2f}'.format).reset_index()

    data = [('Gender Distribution (%)', g, ['Gender', 'Percentage (%)']),('Average Spending per Loyalty Tier', t, ['Tier', 'Avg Spending ($)'])]
    for title, df, col in data:
        fig, ax = plt.subplots(figsize=(6,2))
        ax.axis('off'); ax.set_title(title, weight='bold'); ax.table(cellText=df.values, colLabels=col, loc='center', cellLoc='center').scale(1,2)
        pdf.savefig(fig, bbox_inches='tight'); plt.close()
