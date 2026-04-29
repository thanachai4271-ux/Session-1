import pandas as pd, matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

c = pd.read_csv('customers_cleaned.csv')
c['m'] = c['membership_status'].str.title()

with PdfPages('Session1_CustomerAnalysis_short.pdf') as pdf:
    ax = pd.cut(c['age'], [17,24,34,44,200], labels=['18-24','25-34','35-44','45+']).value_counts().sort_index().plot.bar(title='Distribution of Customer Age Groups', rot=0); ax.set_ylabel('Number of Customers'); ax.grid(axis='y', ls='--', alpha=0.5)
    pdf.savefig(plt.gcf(), bbox_inches='tight'); plt.close()

    g = c[c['gender'].isin(['M','F'])]['gender'].value_counts(normalize=True).mul(100).round(2).reset_index()
    t = c[c['m'].isin(['Basic','Silver','Gold'])].groupby('m')['total_spending'].mean().round(2).reindex(['Basic','Silver','Gold']).reset_index()

    items = [('Gender Distribution (%)', g, ['Gender', 'Percentage (%)']),('Average Spending per Loyalty Tier', t, ['Tier', 'Avg Spending ($)'])]
    
    for title, df, cols in items:
        fig, ax = plt.subplots(figsize=(6,2)) 
        ax.axis('off'); ax.set_title(title, fontsize=13, fontweight='bold', pad=16); ax.table(cellText=df.values, colLabels=cols, loc='center', cellLoc='center').scale(1,2)
        pdf.savefig(fig, bbox_inches='tight'); plt.close()
