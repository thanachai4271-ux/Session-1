import pandas as pd; from statsmodels.tsa.arima.model import ARIMA; import warnings; warnings.filterwarnings('ignore')

s = pd.read_csv('sales_transactions_cleaned.csv')
s['date'] = pd.to_datetime(s['date']).dt.normalize()
d = s.assign(r=s.quantity*s.price-s.discount_amount.fillna(0)).groupby('date')['r'].sum().sort_index()

p = int(len(d)*.8); f = lambda x,n: ARIMA(x, order=(1,1,1)).fit().forecast(steps=n)
print(f"MAE: {(d.iloc[p:] - f(d.iloc[:p], len(d)-p)).abs().mean().round(2)}")

pd.DataFrame({'Date': pd.date_range(d.index[-1] + pd.Timedelta(days=1), periods=30).strftime('%Y-%m-%d'),'Predicted_Sales': f(d, 30).values.round(2)}).to_csv('Session1_SalesForecast_short.csv', index=False)
