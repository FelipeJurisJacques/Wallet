import os
import pandas as pd
from prophet import Prophet

# Criar um dataframe com dados de exemplo
df = pd.read_csv(
    os.path.join(os.path.dirname(__file__), 'data.csv'),
    parse_dates=['ds'],
)

# Criar um modelo Prophet
m = Prophet()

# Treinar o modelo com os dados
m.fit(df)

# Fazer previsões para os próximos 30 dias
future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)

# Plotar os resultados
m.plot(forecast)

print(forecast.tail(30))