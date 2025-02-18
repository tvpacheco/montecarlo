import streamlit as st
import numpy as np
import datetime

# Mapeamento dos multiplicadores de escopo
multiplicadores_escopo = {
    "Claro e compreendido": (1.0, 1.0),
    "Um pouco compreendido": (1.0, 1.5),
    "Não realmente compreendido ainda": (1.5, 2.0),
    "Muito pouco claro ou compreendido": (1.75, 3.0)
}

def simular_previsao(n_simulacoes, min_historias, max_historias, prob_split, min_splits, max_splits,
                     prob_dependencia, atrasos_espera, data_inicio, foco_trabalho, semanas_estimacao,
                     vazao_mensal, impacto_escopo):
    resultados = []
    
    # Obter os multiplicadores baixo e alto para o escopo selecionado
    mult_baixo, mult_alto = multiplicadores_escopo[impacto_escopo]

    # Garantir que a quantidade de semanas seja válida
    semanas_estimacao = min(semanas_estimacao, len(vazao_mensal))

    # Transformar vazão mensal em throughput diário considerando o foco do trabalho
    historico_throughput = np.array(vazao_mensal[-semanas_estimacao:]) / 30 * (foco_trabalho / 100)

    # Aplicar variabilidade usando um multiplicador aleatório dentro do intervalo definido
    variabilidade = np.random.uniform(mult_baixo, mult_alto, size=len(historico_throughput))
    historico_throughput *= variabilidade

    # Evitar throughput muito baixo ou zero
    historico_throughput = np.clip(historico_throughput, 0.1, None)

    for _ in range(n_simulacoes):
        backlog = np.random.randint(min_historias, max_historias + 1)
        dias = 0
        entregues = 0

        while entregues < backlog:
            # Simula splits de histórias
            if np.random.rand() < prob_split:
                backlog += np.random.randint(min_splits, max_splits + 1)
            
            # Simula atrasos devido a dependências externas
            if np.random.rand() < prob_dependencia:
                atraso = np.random.randint(min(atrasos_espera), max(atrasos_espera) + 1)
                dias += atraso
            
            # Simula a entrega de histórias
            throughput = np.random.choice(historico_throughput)
            entregues += max(1, int(throughput))  # Garante pelo menos 1 história entregue por dia
            dias += 1  

        resultados.append(dias)
    
    # Calcular os percentis de 0 a 95 com intervalo de 5
    percentis = {p: data_inicio + datetime.timedelta(days=int(np.percentile(resultados, p))) for p in range(0, 96, 5)}
    return percentis

# Interface Streamlit
st.title("📊 Simulação de Previsibilidade de Entrega - Monte Carlo")

# Entradas do usuário
data_inicio = st.date_input("📅 Data de Início", value=datetime.date(2025, 4, 1))
foco_trabalho = st.slider("🕒 Foco do Trabalho (%)", 10, 100, 100, 5)
semanas_estimacao = st.slider("📈 Semanas para Estimativa", 1, 4, 4)

# Clareza do escopo com os novos valores
escopo_opcao = st.selectbox("📌 Clareza do Escopo", list(multiplicadores_escopo.keys()), index=1)

n_simulacoes = st.slider("🔄 Número de Simulações", 100, 10000, 5000, 100)
min_historias = st.slider("📉 Mínimo de Histórias", 1, 50, 1)
max_historias = st.slider("📈 Máximo de Histórias", min_historias, 50, 1)

# Configuração de splits
st.subheader("🔀 Configuração de Splits")
prob_split = st.slider("📊 Probabilidade de Split (%)", 0, 100, 10) / 100
min_splits = st.slider("📉 Mínimo de Splits", 1, 5, 1)
max_splits = st.slider("📈 Máximo de Splits", min_splits, 5, 1)

# Configuração de dependências externas
st.subheader("⏳ Dependências Externas")
prob_dependencia = st.slider("🚦 Probabilidade de Dependência Externa (%)", 0, 100, 0) / 100
atrasos_espera = [st.number_input(f"🕒 Atraso {i + 1} (dias)", 0, 30, 15) for i in range(5)]

# Histórico de vazão do time
st.subheader("📊 Histórico de Vazão do Time")
vazao_mensal = [st.number_input(f"📆 Período {i + 1}", 0, 50, 5) for i in range(9)]

# Rodar simulação
if st.button("🚀 Rodar Simulação"):
    percentis = simular_previsao(n_simulacoes, min_historias, max_historias, prob_split, min_splits,
                                 max_splits, prob_dependencia, atrasos_espera, data_inicio, foco_trabalho,
                                 semanas_estimacao, vazao_mensal, escopo_opcao)
    
    # Exibir resultados
    st.subheader("📅 Resultados da Simulação")
    for p, data in percentis.items():
        st.write(f"**P{p}:** {data.strftime('%d/%m/%Y')}")
