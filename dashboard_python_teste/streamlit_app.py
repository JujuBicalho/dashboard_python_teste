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

# Título do app
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: white;
        background-color: #003B70;
        padding: 15px;
        border-radius: 5px;
        font-size: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
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

# Exibindo métricas com design restaurado
st.markdown("### Métricas Gerais")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div style="background-color:#E8F4FF; padding:10px; border-radius:10px; text-align:center; border:1px solid #003B70;">
            <h4 style="color:#003B70;">Total de Transações 💳</h4>
            <h2 style="color:#003B70;">{total_transacoes}</h2>
            <p>Valor total movimentado por todas as transações no período.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div style="background-color:#F0F8FF; padding:10px; border-radius:10px; text-align:center; border:1px solid #007ACC;">
            <h4 style="color:#007ACC;">Gasto Médio por Transação 📊</h4>
            <h2 style="color:#007ACC;">{media_gasto}</h2>
            <p>Média do valor gasto em cada transação.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div style="background-color:#FFE8E8; padding:10px; border-radius:10px; text-align:center; border:1px solid #CC0000;">
            <h4 style="color:#CC0000;">Total de Inadimplentes 🚨</h4>
            <h2 style="color:#CC0000;">{total_inadimplentes}</h2>
            <p>Número de clientes inadimplentes no período analisado.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div style="background-color:#E8FFE8; padding:10px; border-radius:10px; text-align:center; border:1px solid #008000;">
            <h4 style="color:#008000;">Total de Cashback Usado 🤑</h4>
            <h2 style="color:#008000;">{total_cashback}</h2>
            <p>Valor total resgatado em benefícios de cashback.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Gráficos
st.markdown("### Gráficos")
st.subheader("Gastos por Categoria")
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
