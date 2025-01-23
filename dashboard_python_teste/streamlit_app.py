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
st.title("Dashboard de Cartões de Crédito")
st.write("Análise de transações, inadimplência e benefícios")

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

# Exibindo métricas
st.subheader("Métricas Gerais")
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total de Transações 💳", total_transacoes)
col2.metric("Gasto Médio por Transação 📊", media_gasto)
col3.metric("Total de Inadimplentes 🚨", f"{total_inadimplentes}")
col4.metric("Total de Cashback Usado 🤑", total_cashback)

# Gráfico de Gastos por Categoria
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

# Gráfico de Inadimplência por Região
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

# Gráfico de Uso de Benefícios
st.subheader("Uso de Benefícios")
beneficios_uso = transacoes_completas.groupby(['Participa_Cashback', 'Participa_Pontos'])['Valor_Transação'].sum().reset_index()
beneficios_uso['Benefício'] = beneficios_uso.apply(
    lambda x: f"Cashback: {'Sim' if x['Participa_Cashback'] else 'Não'}, Pontos: {'Sim' if x['Participa_Pontos'] else 'Não'}", axis=1
)
fig_beneficios = px.bar(
    beneficios_uso,
    x='Benefício',
    y='Valor_Transação',
    text_auto=True,
    title="Uso de Benefícios",
    labels={'Valor_Transação': 'Total (R$)', 'Benefício': 'Benefício'}
)
fig_beneficios.update_layout(title_x=0.5)
st.plotly_chart(fig_beneficios, use_container_width=True)

# Observações e Sugestões
st.subheader("Observações e Sugestões")
st.write("""
- **Clientes Gold** têm maior concentração de gastos em 'Alimentação'. Sugerimos criar parcerias com redes de restaurantes e supermercados para oferecer cashback dedicado a essas transações.
- **Clientes Black** concentram maior parte dos gastos em 'Viagem'. Desenvolva promoções de passagens aéreas, hotéis e pacotes turísticos.
- A **região Sudeste** concentra a maior parte dos inadimplentes. Reforce a análise de crédito e implemente campanhas de educação financeira nessa região.
- **Clientes com cashback** gastam, em média, 30% mais. Expanda o programa para novas categorias.
- Muitos clientes acumulam pontos, mas não realizam o resgate. Envie notificações automáticas e promova campanhas para incentivar o uso de pontos.
""")
