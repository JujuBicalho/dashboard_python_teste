import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Fixando a semente para valores aleatórios consistentes
np.random.seed(42)

# Cache para dados simulados
@st.cache_data
def carregar_dados():
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

    return transacoes, clientes, beneficios, transacoes_completas


# Carregando os dados
transacoes, clientes, beneficios, transacoes_completas = carregar_dados()

# Função para formatar valores
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Estilo CSS para responsividade
st.markdown(
    """
    <style>
    .title {
        text-align: center;
        color: white;
        background-color: #003B70;
        padding: 15px;
        border-radius: 5px;
        font-size: 2em;
    }
    .metric-card {
        background-color: #f9f9f9;
        padding: 10px;
        border-radius: 10px;
        margin: 10px;
        text-align: center;
        border: 1px solid #ddd;
        flex: 1 1 calc(25% - 20px);
        box-sizing: border-box;
    }
    .metric-row {
        display: flex;
        flex-wrap: wrap;
        justify-content: space-around;
    }
    .metric-title {
        font-size: 1.2em;
        margin-bottom: 5px;
        color: #333;
    }
    .metric-value {
        font-size: 2em;
        font-weight: bold;
        margin: 10px 0;
        color: #003B70;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Título do app
st.markdown('<div class="title">Dashboard de Cartões de Crédito</div>', unsafe_allow_html=True)
st.subheader("Análise de transações, inadimplência e benefícios")

# Filtros
tipo_cartao = st.selectbox(
    "Selecione o Tipo de Cartão:",
    options=['Todos', 'Gold', 'Platinum', 'Black']
)

# Filtrar os dados
dados_filtrados = transacoes if tipo_cartao == 'Todos' else transacoes[transacoes['Tipo_Cartão'] == tipo_cartao]

# Criando as abas
tab1, tab2 = st.tabs(["Métricas e Gráficos", "Sugestões e Observações"])

# Conteúdo da aba 1
with tab1:
    # Métricas principais
    st.markdown(
        f"""
        <div class="metric-row">
            <div class="metric-card" style="background-color: #E8F4FF;">
                <div class="metric-title">Total de Transações 💳</div>
                <div class="metric-value">{formatar_valor(dados_filtrados['Valor_Transação'].sum())}</div>
                <small>Valor total movimentado no período.</small>
            </div>
            <div class="metric-card" style="background-color: #F0F8FF;">
                <div class="metric-title">Gasto Médio por Transação 📊</div>
                <div class="metric-value">{formatar_valor(dados_filtrados['Valor_Transação'].mean())}</div>
                <small>Média do valor gasto por transação.</small>
            </div>
            <div class="metric-card" style="background-color: #FFE8E8;">
                <div class="metric-title">Total de Inadimplentes 🚨</div>
                <div class="metric-value">{clientes['Status_Inadimplente'].sum()}</div>
                <small>Número de clientes inadimplentes.</small>
            </div>
            <div class="metric-card" style="background-color: #E8FFE8;">
                <div class="metric-title">Total de Cashback Usado 🤑</div>
                <div class="metric-value">{formatar_valor(transacoes_completas[transacoes_completas['Participa_Cashback'] == 1]['Valor_Transação'].sum())}</div>
                <small>Total resgatado em benefícios.</small>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Gráficos
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
    fig_categoria.update_layout(title_text="Gastos por Categoria", title_x=0.5)
    st.plotly_chart(fig_categoria, use_container_width=True)

    st.subheader("Inadimplência por Região")
    inadimplentes = clientes[clientes['Status_Inadimplente'] == 1]
    grafico_inadimplencia = inadimplentes.groupby('Região')['ID_Cliente'].count().reset_index()
    fig_inadimplencia = px.pie(
        grafico_inadimplencia,
        values='ID_Cliente',
        names='Região',
        title="Distribuição de Inadimplência por Região",
        labels={'ID_Cliente': 'Clientes'},
        color_discrete_sequence=px.colors.sequential.Reds
    )
    fig_inadimplencia.update_layout(title_text="Distribuição de Inadimplência por Região", title_x=0.5)
    st.plotly_chart(fig_inadimplencia, use_container_width=True)

# Conteúdo da aba 2
with tab2:
    st.subheader("Sugestões e Observações")
    st.write("""
    - Clientes **Gold** têm maior concentração de gastos em 'Alimentação'. Parcerias com restaurantes podem aumentar a fidelidade.
    - Clientes **Black** gastam mais em 'Viagem'. Promoções em hotéis e passagens podem atrair novos clientes.
    - A região **Sudeste** concentra a maior parte dos inadimplentes. Reforce análises de crédito e políticas na região.
    - **Cashback** é atrativo: participantes gastam, em média, 25% a mais. Expanda para outras categorias.
    """)
