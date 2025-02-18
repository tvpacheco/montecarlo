import streamlit as st
import numpy as np
import datetime

def simular_previsao(n_simulacoes, min_historias, max_historias, prob_split, min_splits, max_splits,
                     data_inicio, foco_trabalho, semanas_estimacao, vazao_semanal, multiplicador_baixo, multiplicador_alto):
    resultados = []
    semanas_estimacao = min(semanas_estimacao, len(vazao_semanal))  # Evita erro de indexação
    historico_throughput = np.array(vazao_semanal[-semanas_estimacao:]) * (foco_trabalho / 100)

    for _ in range(n_simulacoes):
        backlog = np.random.randint(min_historias, max_historias + 1)  
        dias = 0
        entregues = 0

        while entregues < backlog:
            if np.random.rand() < prob_split:
                backlog += np.random.randint(min_splits, max_splits + 1)

            throughput = np.random.choice(historico_throughput) * np.random.uniform(multiplicador_baixo, multiplicador_alto)
            entregues += throughput
            dias += 7  # Contabilizando semanas inteiras para cada ciclo

        resultados.append(dias)

    percentis = {p: data_inicio + datetime.timedelta(days=int(np.percentile(resultados, p))) for p in range(0, 96, 5)}
    return percentis

# Interface no Streamlit
st.title("Simulação de Previsibilidade de Entrega")
data_inicio = st.date_input("Data de Início", value=datetime.date(2025, 4, 1))
foco_trabalho = st.slider("Foco do Trabalho (%)", 10, 100, 75, 5)
semanas_estimacao = st.slider("Semanas para Estimativa", 1, 4, 4)
n_simulacoes = st.slider("Número de Simulações", 100, 10000, 5000, 100)
min_historias = st.slider("Mínimo de Histórias", 1, 50, 15)
max_historias = st.slider("Máximo de Histórias", min_historias, 50, 30)
prob_split = st.slider("Probabilidade de Split (%)", 0, 100, 10) / 100
min_splits = st.slider("Mínimo de Splits", 1, 5, 1)
max_splits = st.slider("Máximo de Splits", min_splits, 5, 1)

# Clareza do escopo e multiplicadores
escopo_opcoes = {
    "Claro e compreendido": (1, 1),
    "Um pouco compreendido": (1, 1.5),
    "Não realmente compreendido ainda": (1.5, 2),
    "Muito pouco claro ou compreendido": (1.75, 3)
}
escopo_escolhido = st.selectbox("Clareza do Escopo", list(escopo_opcoes.keys()))
multiplicador_baixo, multiplicador_alto = escopo_opcoes[escopo_escolhido]

# Histórico de vazão semanal
st.subheader("Histórico de Vazão (semanas)")
vazao_semanal = [st.number_input(f"Semana {i + 1}", 0, 50, val) for i, val in enumerate([9, 4, 12, 14, 4, 3, 3, 10, 9])]

if st.button("Rodar Simulação"):
    percentis = simular_previsao(n_simulacoes, min_historias, max_historias, prob_split, min_splits,
                                 max_splits, data_inicio, foco_trabalho, semanas_estimacao,
                                 vazao_semanal, multiplicador_baixo, multiplicador_alto)
    
    st.write("### Resultados da Simulação")
    for p, data in percentis.items():
        st.write(f"**P{p}:** {data}")
