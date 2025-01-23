
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Dados simulados
transacoes = pd.DataFrame({
    'Data_Transação': pd.date_range(start='2024-01-01', periods=1000, freq='D'),
    'ID_Cliente': np.random.randint(1, 101, size=1000),
    'Tipo_Cartão': np.random.choice(['Gold', 'Platinum', 'Black'], size=1000, p=[0.5, 0.3, 0.2]),
    'Valor_Transação': np.random.uniform(50, 2000, size=1000).round(2),
    'Categoria_Gasto': np.random.choice(['Alimentação', 'Viagem', 'Compras Online', 'Educação'], size=1000),
    'Limite_Cartão': np.random.uniform(5000, 20000, size=1000).round(-2)
})

clientes = pd.DataFrame({
    'ID_Cliente': range(1, 101),
    'Idade': np.random.randint(18, 65, size=100),
    'Renda_Mensal': np.random.uniform(2000, 15000, size=100).round(-2),
    'Status_Inadimplente': np.random.choice([0, 1], size=100, p=[0.85, 0.15]),
    'Tipo_Cartão': np.random.choice(['Gold', 'Platinum', 'Black'], size=100, p=[0.5, 0.3, 0.2]),
    'Região': np.random.choice(['Norte', 'Sul', 'Sudeste', 'Nordeste'], size=100)
})

beneficios = pd.DataFrame({
    'ID_Cliente': range(1, 101),
    'Participa_Cashback': np.random.choice([0, 1], size=100, p=[0.4, 0.6]),
    'Participa_Pontos': np.random.choice([0, 1], size=100, p=[0.3, 0.7]),
    'Saldo_Pontos': np.random.randint(0, 5000, size=100)
})

transacoes_completas = pd.merge(transacoes, beneficios, on='ID_Cliente')

# Função para formatar valores
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Estilo CSS para centralizar e organizar o layout
st.markdown(
    """
    <style>
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 0 20px;
    }
    .title {
        text-align: center;
        color: white;
        background-color: #003B70;
        padding: 15px;
        border-radius: 5px;
        font-size: 2em;
        margin-bottom: 20px;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        gap: 20px;
        flex-wrap: wrap;
    }
    .metric-card {
        flex: 1;
        min-width: 220px;
        background-color: #f9f9f9;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #ddd;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Layout principal
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<div class="title">Dashboard de Cartões de Crédito</div>', unsafe_allow_html=True)

st.subheader("Análise de transações, inadimplência e benefícios")

# Filtros
tipo_cartao = st.selectbox(
    "Selecione o Tipo de Cartão:",
    options=['Todos', 'Gold', 'Platinum', 'Black']
)

# Filtrar os dados
dados_filtrados = transacoes if tipo_cartao == 'Todos' else transacoes[transacoes['Tipo_Cartão'] == tipo_cartao]

# Métricas principais
total_transacoes = formatar_valor(dados_filtrados['Valor_Transação'].sum())
media_gasto = formatar_valor(dados_filtrados['Valor_Transação'].mean())
total_inadimplentes = clientes['Status_Inadimplente'].sum()
total_cashback = formatar_valor(
    transacoes_completas[transacoes_completas['Participa_Cashback'] == 1]['Valor_Transação'].sum()
)

# Exibindo métricas centralizadas
st.markdown("### Métricas Gerais")
st.markdown('<div class="metric-container">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="metric-card" style="background-color: #E8F4FF;">
        <h4>Total de Transações 💳</h4>
        <h2>{total_transacoes}</h2>
        <p>Valor total movimentado no período.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <div class="metric-card" style="background-color: #F0F8FF;">
        <h4>Gasto Médio por Transação 📊</h4>
        <h2>{media_gasto}</h2>
        <p>Média do valor gasto por transação.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <div class="metric-card" style="background-color: #FFE8E8;">
        <h4>Total de Inadimplentes 🚨</h4>
        <h2>{total_inadimplentes}</h2>
        <p>Número de clientes inadimplentes.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown(
    f"""
    <div class="metric-card" style="background-color: #E8FFE8;">
        <h4>Total de Cashback Usado 🤑</h4>
        <h2>{total_cashback}</h2>
        <p>Total resgatado em benefícios.</p>
    </div>
    """,
    unsafe_allow_html=True
)
st.markdown('</div>', unsafe_allow_html=True)

# Gráficos
st.subheader("Gráficos")
grafico_categorias = dados_filtrados.groupby('Categoria_Gasto')['Valor_Transação'].sum().reset_index()
fig_categoria = px.bar(
    grafico_categorias,
    x='Categoria_Gasto',
    y='Valor_Transação',
    text_auto=True,
    title="Gastos por Categoria",
    labels={'Categoria_Gasto': 'Categoria', 'Valor_Transação': 'Total (R$)'}
)
fig_categoria.update_layout(title_x=0.5)
st.plotly_chart(fig_categoria, use_container_width=True)

st.subheader("Distribuição de Inadimplência por Região")
inadimplentes = clientes[clientes['Status_Inadimplente'] == 1]
grafico_inadimplencia = inadimplentes.groupby('Região')['ID_Cliente'].count().reset_index()
fig_inadimplencia = px.pie(
    grafico_inadimplencia,
    values='ID_Cliente',
    names='Região',
    title="Inadimplência por Região",
    labels={'ID_Cliente': 'Clientes'},
    color_discrete_sequence=px.colors.sequential.Reds
)
fig_inadimplencia.update_layout(title_x=0.5)
st.plotly_chart(fig_inadimplencia, use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)
