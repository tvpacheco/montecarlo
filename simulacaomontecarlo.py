import numpy as np
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

def monte_carlo_forecast(throughput_history, start_date, min_stories, max_stories, num_simulations=10000):
    """
    Simula previsões de entrega com base no throughput histórico e distribuições Monte Carlo.
    """
    simulated_dates = []
    
    for _ in range(num_simulations):
        total_stories = np.random.randint(min_stories, max_stories + 1)
        days_elapsed = 0
        stories_delivered = 0
        
        while stories_delivered < total_stories:
            weekly_throughput = np.random.choice(throughput_history)
            stories_delivered += weekly_throughput
            days_elapsed += 7  # Considera semanas completas
        
        delivery_date = start_date + timedelta(days=days_elapsed)
        simulated_dates.append(delivery_date)
    
    return simulated_dates

def get_forecast_dates(simulated_dates):
    """
    Calcula percentis para previsão de datas.
    """
    percentiles = [100, 95, 90, 85, 80, 75, 70, 65, 60, 55, 50, 45, 40, 35, 30, 25, 20, 15, 10, 5, 0]
    forecast_results = {p: np.percentile(simulated_dates, p, interpolation='nearest') for p in percentiles}
    
    return forecast_results

# Parâmetros fornecidos pelo usuário
throughput_history = [9, 4, 12, 14, 4, 3, 3, 10, 9]
start_date = datetime(2025, 4, 1)
min_stories = 15
max_stories = 30

# Simulação Monte Carlo
simulated_dates = monte_carlo_forecast(throughput_history, start_date, min_stories, max_stories)
forecast_results = get_forecast_dates(simulated_dates)

# Exibir os resultados no Streamlit
st.title("Previsibilidade de Datas de Entrega - Modelo Troy Magennis")

df_results = pd.DataFrame.from_dict(forecast_results, orient='index', columns=['Data Prevista'])
df_results.index.name = 'Probabilidade (%)'
df_results = df_results.sort_index(ascending=False)

df_results['Data Prevista'] = df_results['Data Prevista'].apply(lambda x: x.strftime('%d/%m/%Y'))

st.table(df_results)
