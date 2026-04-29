import pandas as pd, warnings; from statsmodels.tsa.arima.model import ARIMA; from sklearn.metrics import mean_absolute_error as E; warnings.filterwarnings('ignore')

s = pd.read_csv('sales_transactions_cleaned.csv')
s['date'] = pd.to_datetime(s['date']).dt.normalize()
d = s.assign(r=s.quantity*s.price-pd.to_numeric(s.discount_amount,'coerce').fillna(0)).groupby('date')['r'].sum().sort_index()

p = int(len(d)*.8); f = lambda x,n: ARIMA(x,order=(1,1,1)).fit().forecast(steps=n)

pd.DataFrame({'Date': pd.date_range(d.index[-1] + pd.Timedelta(days=1), periods=30).strftime('%Y-%m-%d'),'Predicted_Sales': f(d, 30).values.round(2)}).to_csv('Session1_SalesForecast_shortv2.csv', index=False)
