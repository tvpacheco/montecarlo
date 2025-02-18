import streamlit as st
import numpy as np
import random
import datetime

# Parâmetros da simulação
historical_throughput = [9, 4, 12, 14, 4, 3, 3, 10, 9]
start_date = datetime.date(2025, 4, 1)
min_stories = 15
max_stories = 30
split_low = 1
split_high = 1
simulated_days = 28  # Período da simulação (4 semanas)

# Multiplicadores de escopo
scope_multipliers = {
    "Claro e compreendido": (1, 1),
    "Um pouco compreendido": (1, 1.5),
    "Ainda não compreendido": (1.5, 2),
    "Muito pouco claro ou compreendido": (1.75, 3)
}

# Criar distribuição cumulativa do throughput
throughput_distribution = np.random.choice(historical_throughput, size=10000, replace=True)

def simulate_delivery(n_simulations=10000, selected_scope="Claro e compreendido"):
    results = []
    low_multiplier, high_multiplier = scope_multipliers[selected_scope]
    
    for _ in range(n_simulations):
        remaining_stories = random.randint(min_stories, max_stories)
        remaining_stories *= random.uniform(low_multiplier, high_multiplier)
        current_date = start_date
        
        while remaining_stories > 0:
            throughput = np.random.choice(throughput_distribution)  # Uso da distribuição cumulativa
            remaining_stories -= throughput
            current_date += datetime.timedelta(weeks=1)
        
        results.append(current_date)
    
    return results

def calculate_percentiles(results):
    percentiles = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
    percentile_dates = {f"P{p}": np.percentile(results, p, method='nearest') for p in percentiles}
    return percentile_dates

# Interface do Streamlit
st.title("Simulação de Previsibilidade - Modelo de Monte Carlo")

selected_scope = st.selectbox("Nível de clareza do escopo:", list(scope_multipliers.keys()))
n_simulations = st.slider("Número de simulações:", min_value=1000, max_value=50000, value=10000, step=5000)

if st.button("Rodar Simulação"):
    st.write("Executando a simulação, aguarde...")
    simulated_results = simulate_delivery(n_simulations, selected_scope)
    percentile_results = calculate_percentiles(simulated_results)

    st.write("### Resultados da Simulação:")
    for key, value in percentile_results.items():
        st.write(f"{key}: {value}")

