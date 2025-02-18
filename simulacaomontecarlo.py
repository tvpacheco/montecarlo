import streamlit as st
import numpy as np
import datetime

# Injetando CSS para deixar os sliders verdes
st.markdown("""
    <style>
        div[data-baseweb="slider"] > div > div {
            background: #4CAF50 !important;  /* Verde */
        }
        div[data-baseweb="slider"] > div > div > div {
            background: #2E7D32 !important;  /* Verde escuro */
        }
    </style>
""", unsafe_allow_html=True)

def simular_previsao(n_simulacoes, min_historias, max_historias, prob_split, min_splits, max_splits,
                     data_inicio, foco_trabalho, semanas_estimacao, vazao_mensal, impacto_escopo):
    resultados = []
    
    # Mapeando impacto do escopo para variação de throughput
    multiplicadores = {
        "Claro e compreendido": (1.0, 1.0),
        "Um pouco compreendido": (1.0, 1.5),
        "Não realmente compreendido ainda": (1.5, 2.0),
        "Muito pouco claro ou compreendido": (1.75, 3.0),
    }
    mult_baixo, mult_alto = multiplicadores[impacto_escopo]

    semanas_estimacao = min(semanas_estimacao, len(vazao_mensal))
    historico_throughput = np.array(vazao_mensal[-semanas_estimacao:]) * (foco_trabalho / 100)

    for _ in range(n_simulacoes):
        backlog = np.random.randint(min_historias, max_historias + 1)  
        dias = 0
        entregues = 0

        while entregues < backlog:
            throughput_semanal = np.random.choice(historico_throughput)
            variacao = np.random.uniform(mult_baixo, mult_alto)
            throughput_semanal *= variacao

            if np.random.rand() < prob_split:
                backlog += np.random.randint(min_splits, max_splits + 1)

            entregues += throughput_semanal
            dias += 7  

        resultados.append(dias)

    percentis = {p: data_inicio + datetime.timedelta(days=int(np.percentile(resultados, p))) for p in range(0, 96, 5)}
    return percentis

# Interface Streamlit
st.title("Simulação de Previsibilidade de Entrega")
data_inicio = st.date_input("Data de Início", value=datetime.date(2025, 4, 1))
foco_trabalho = st.slider("Foco do Trabalho (%)", 10, 100, 75, 5)
semanas_estimacao = st.slider("Semanas para Estimativa", 1, 4, 4)
escopo_opcao = st.selectbox("Clareza do Escopo", [
    "Claro e compreendido", 
    "Um pouco compreendido", 
    "Não realmente compreendido ainda", 
    "Muito pouco claro ou compreendido"
], index=0)
n_simulacoes = st.slider("Número de Simulações", 100, 10000, 5000, 100)
min_historias = st.slider("Mínimo de Histórias", 1, 50, 15)
max_historias = st.slider("Máximo de Histórias", min_historias, 50, 30)
prob_split = st.slider("Probabilidade de Split (%)", 0, 100, 10) / 100
min_splits = st.slider("Mínimo de Splits", 1, 5, 1)
max_splits = st.slider("Máximo de Splits", min_splits, 5, 1)

st.subheader("Histórico de Vazão Semanal")
vazao_mensal = [st.number_input(f"Semana {i + 1}", 0, 50, v) for i, v in enumerate([9, 4, 12, 14, 4, 3, 3, 10, 9])]

if st.button("Rodar Simulação"):
    percentis = simular_previsao(n_simulacoes, min_historias, max_historias, prob_split, min_splits,
                                 max_splits, data_inicio, foco_trabalho, semanas_estimacao, vazao_mensal, escopo_opcao)
    
    st.write(f"### Simulação realizada: {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    for p, data in percentis.items():
        st.write(f"**P{p}:** {data}")
