import streamlit as st
import numpy as np
import datetime
#import matplotlib.pyplot as plt

def simular_previsao(n_simulacoes, qtd_itens_trabalho, min_historias, max_historias, prob_split, min_splits, max_splits,
                     prob_dependencia, media_espera, desvio_espera, data_inicio, foco_trabalho, semanas_estimacao,
                     vazao_mensal, impacto_escopo):
    resultados = []
    variabilidade = {'Baixo': 1.2, 'Médio': 1.0, 'Alto': 0.9}[impacto_escopo]
    semanas_estimacao = min(semanas_estimacao, len(vazao_mensal))  # Evita erro de indexação
    historico_throughput = np.array(vazao_mensal[-semanas_estimacao:]) / 22 * (foco_trabalho / 100) * variabilidade
    historico_throughput = np.maximum(np.round(historico_throughput), 1).astype(int)  # Garante valores inteiros

    for _ in range(n_simulacoes):
        backlog = np.random.randint(min_historias, max_historias + 1)  # Definir o backlog inicial dentro do intervalo
        dias = 0
        entregues = 0

        while entregues < backlog:
            if np.random.rand() < prob_split:
                backlog += min(np.random.randint(min_splits, max_splits + 1), 2 * qtd_itens_trabalho)  # Evita backlog infinito
            
            if np.random.rand() < prob_dependencia:
                dias += max(0, int(np.random.normal(media_espera, desvio_espera)))  # Evita valores negativos
            
            entregues += np.random.choice(historico_throughput)
            
            # Conta apenas dias úteis (5 dias por semana)
            dias += 1
            if dias % 7 in [5, 6]:  # Se cair no fim de semana, pula para segunda-feira
                dias += (7 - dias % 7)

        resultados.append(dias)

    percentis = {p: data_inicio + datetime.timedelta(days=int(np.percentile(resultados, p))) for p in range(0, 96, 5)}
    return percentis, resultados

st.title("Simulação de Previsibilidade de Entrega")
data_inicio = st.date_input("Data de Início", value=datetime.date(2025, 4, 1))
foco_trabalho = st.slider("Foco do Trabalho (%)", 10, 100, 100, 5)
semanas_estimacao = st.slider("Semanas para Estimativa", 1, 4, 4)
escopo_opcao = st.selectbox("Clareza do Escopo", ["Baixo", "Médio", "Alto"], index=1)
n_simulacoes = st.slider("Número de Simulações", 100, 10000, 5000, 100)
qtd_itens_trabalho = st.slider("Quantidade de Itens de Trabalho", 1, 50, 1)
min_historias = st.slider("Mínimo de Histórias", 1, 50, 1)
max_historias = st.slider("Máximo de Histórias", min_historias, 50, 1)
prob_split = st.slider("Probabilidade de Split (%)", 0, 100, 10) / 100
min_splits = st.slider("Mínimo de Splits", 1, 5, 1)
max_splits = st.slider("Máximo de Splits", min_splits, 5, 1)
prob_dependencia = st.slider("Probabilidade de Dependência Externa (%)", 0, 100, 20) / 100
media_espera = st.slider("Tempo Médio de Espera (dias)", 0, 30, 0)
desvio_espera = st.slider("Desvio Padrão da Espera (dias)", 0, 10, 0)
st.subheader("Histórico de Vazão")
vazao_mensal = [st.number_input(f"Período {i + 1}", 0, 50, 5) for i in range(9)]

if st.button("Rodar Simulação"):
    percentis, resultados = simular_previsao(n_simulacoes, qtd_itens_trabalho, min_historias, max_historias, prob_split, min_splits,
                                             max_splits, prob_dependencia, media_espera, desvio_espera, data_inicio, foco_trabalho,
                                             semanas_estimacao, vazao_mensal, escopo_opcao)
    data_hora_simulacao = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    st.write(f"### Simulação realizada em {data_hora_simulacao}")
    st.write("### Resultados da Simulação")
    for p, data in percentis.items():
        st.write(f"**P{p}:** {data}")
    
    # Plotando a distribuição dos resultados
    #fig, ax = plt.subplots()
   # ax.hist(resultados, bins=30, edgecolor='black', alpha=0.7)
   # ax.set_title("Distribuição dos Dias de Entrega")
   # ax.set_xlabel("Dias")
   # ax.set_ylabel("Frequência")
   # st.pyplot(fig, clear_figure=True)
