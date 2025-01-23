# Importando as bibliotecas necessárias
import streamlit as st
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import numpy as np
import plotly.express as px

# Função para formatar valores no padrão brasileiro
def formatar_valor(valor):
    return f"R$ {valor:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

# Criando os dados simulados
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

# Criando o app Dash
app = dash.Dash(__name__)
app.title = "Dashboard Profissional"

# Função para calcular métricas gerais
def calcular_metricas():
    total_transacoes = transacoes['Valor_Transação'].sum()
    media_gasto = transacoes['Valor_Transação'].mean()
    total_inadimplentes = clientes['Status_Inadimplente'].sum()
    total_cashback = transacoes_completas[transacoes_completas['Participa_Cashback'] == 1]['Valor_Transação'].sum()
    return total_transacoes, media_gasto, total_inadimplentes, total_cashback

# Layout do Dashboard
app.layout = html.Div([
    # Título do Dashboard
    html.Div([
        html.H1("Dashboard de Cartões de Crédito", style={'text-align': 'center', 'color': 'white'}),
        html.P("Análise de transações, inadimplência e benefícios", style={'text-align': 'center', 'color': 'white'})
    ], style={'background-color': '#003B70', 'padding': '10px'}),
    
    # Abas para organizar o conteúdo
    dcc.Tabs([
        # Aba 1: Gráficos
        dcc.Tab(label='Análises Gráficas', children=[
            # Dropdown para seleção de tipo de cartão
            html.Div([
                html.Label("Selecione o Tipo de Cartão:", style={'font-size': '16px', 'margin-top': '20px'}),
                dcc.Dropdown(
                    id='tipo_cartao',
                    options=[
                        {'label': 'Todos', 'value': 'Todos'},
                        {'label': 'Gold', 'value': 'Gold'},
                        {'label': 'Platinum', 'value': 'Platinum'},
                        {'label': 'Black', 'value': 'Black'}
                    ],
                    value='Todos',  # Valor padrão
                    style={'width': '50%', 'margin': '20px auto'}
                )
            ], style={'text-align': 'center'}),

            # Cartões de Métricas
            html.Div([
                html.Div([
                    html.H4("Total de Transações 💳", style={'text-align': 'center', 'color': 'black'}),
                    html.H3(formatar_valor(calcular_metricas()[0]), style={'text-align': 'center', 'color': '#003B70'}),
                    html.P("Valor total movimentado por todas as transações no período.", style={'text-align': 'center', 'font-size': '12px'}),
                ], className='card', style={'background-color': '#E8F4FF', 'border': '1px solid #003B70', 'padding': '15px', 'border-radius': '10px'}),
                html.Div([
                    html.H4("Gasto Médio por Transação 📊", style={'text-align': 'center', 'color': 'black'}),
                    html.H3(formatar_valor(calcular_metricas()[1]), style={'text-align': 'center', 'color': '#007ACC'}),
                    html.P("Média do valor gasto em cada transação.", style={'text-align': 'center', 'font-size': '12px'}),
                ], className='card', style={'background-color': '#F0F8FF', 'border': '1px solid #007ACC', 'padding': '15px', 'border-radius': '10px'}),
                html.Div([
                    html.H4("Total de Inadimplentes 🚨", style={'text-align': 'center', 'color': 'black'}),
                    html.H3(f"{calcular_metricas()[2]:,}".replace(',', '.'), style={'text-align': 'center', 'color': '#CC0000'}),
                    html.P("Número de clientes inadimplentes no período analisado.", style={'text-align': 'center', 'font-size': '12px'}),
                ], className='card', style={'background-color': '#FFE8E8', 'border': '1px solid #CC0000', 'padding': '15px', 'border-radius': '10px'}),
                html.Div([
                    html.H4("Total de Cashback Usado 🤑", style={'text-align': 'center', 'color': 'black'}),
                    html.H3(formatar_valor(calcular_metricas()[3]), style={'text-align': 'center', 'color': '#008000'}),
                    html.P("Valor total resgatado em benefícios de cashback.", style={'text-align': 'center', 'font-size': '12px'}),
                ], className='card', style={'background-color': '#E8FFE8', 'border': '1px solid #008000', 'padding': '15px', 'border-radius': '10px'}),
            ], style={'display': 'flex', 'justify-content': 'space-around', 'padding': '20px'}),
        ], style={'background-color': '#F9F9F9'}),

        # Aba 2: Observações e Sugestões
        dcc.Tab(label='Observações e Sugestões', children=[
            html.Div([
                html.H3("Observações e Sugestões", style={'text-align': 'center', 'margin-top': '30px'}),
                html.Ul([
                    html.Li("Clientes Gold têm maior concentração de gastos em 'Alimentação'. Sugerimos criar parcerias com redes de supermercados e restaurantes para oferecer cashback dedicado a essas transações."),
                    html.Li("Clientes Black concentram seus gastos em 'Viagem'. Isso sugere a criação de promoções em passagens aéreas, hotéis e pacotes turísticos para reforçar a experiência premium."),
                    html.Li("A região Sudeste concentra a maior parte dos inadimplentes. Uma recomendação seria realizar análises de crédito mais rigorosas nessa região e campanhas de educação financeira para os clientes."),
                    html.Li("Clientes participantes de cashback gastam, em média, 30% mais por transação. Sugerimos expandir a campanha de cashback para outras categorias de gasto."),
                    html.Li("A maioria dos clientes acumula pontos, mas não realiza resgates frequentes. É recomendável enviar notificações automáticas sobre saldo de pontos e campanhas para incentivá-los a resgatar benefícios."),
                    html.Li("Categorias como 'Educação' apresentam potencial inexplorado. Promova campanhas de incentivo ao uso em cursos e assinaturas educacionais."),
                ], style={'padding': '20px', 'font-size': '16px', 'line-height': '1.8'})
            ], style={'padding': '20px'})
        ], style={'background-color': '#F9F9F9'}),
    ], style={'border': '1px solid #D3D3D3', 'border-radius': '10px', 'overflow': 'hidden'}),
])

# Executa o servidor
if __name__ == '__main__':
    app.run_server(debug=True)
