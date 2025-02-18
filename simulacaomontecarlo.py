import streamlit as st
import numpy as np
import random
import datetime

# Parâmetros da simulação
historical_throughput = [9, 4, 12, 14, 4, 3, 3, 10, 9]
start_date = datetime.date(2025, 4, 1)
simulated_days = 28  # Período da simulação (4 semanas)

# Multiplicadores de escopo
scope_multipliers = {
    "Claro e compreendido": (1, 1),
    "Um pouco compreendido": (1, 1.5),
    "Ainda não compreendido": (1.5, 2),
    "Muito pouco claro ou compreendido": (1.75, 3)
}

# Configuração da Interface no Streamlit
st.title("Simulação de Previsibilidade de Entrega")

# Entrada de parâmetros do usuário
selected_scope = st.selectbox(
    "Nível de compreensão do escopo:",
    list(scope_multipliers.keys()),
)

low_multiplier, high_multiplier = scope_multipliers[selected_scope]

min_stories = st.slider("Quantidade mínima de histórias", 10, 50, 15)
max_stories = st.slider("Quantidade máxima de histórias", 20, 60, 30)

split_low = st.slider("Mínimo de splits por história", 1, 5, 1)
split_high = st.slider("Máximo de splits por história", 1, 5, 1)

n_simulations = st.number_input("Número de Simulações", min_value=1000, max_value=50000, value=10000, step=1000)

# Função de simulação
def simulate_delivery(n_simulations):
    results = []
    for _ in range(n_simulations):
        remaining_stories = random.randint(min_stories, max_stories)
        remaining_stories *= random.uniform(low_multiplier, high_multiplier)
        current_date = start_date

        while remaining_stories > 0:
            throughput = random.choice(historical_throughput)
            remaining_stories -= throughput
            current_date += datetime.timedelta(weeks=1)

        results.append(current_date)

    return results

# Função para calcular percentis
def calculate_percentiles(results):
    percentiles = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
    percentile_dates = {f"P{p}": np.percentile(results, p, method='nearest') for p in percentiles}
    return percentile_dates

# Botão para rodar a simulação
if st.button("Rodar Simulação"):
    simulated_results = simulate_delivery(n_simulations)
    percentile_results = calculate_percentiles(simulated_results)

    # Exibir resultados
    st.subheader("Resultados da Simulação")
    for key, value in percentile_results.items():
        st.write(f"{key}: {value}")
