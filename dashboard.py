import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página do Streamlit para layout responsivo
st.set_page_config(layout="wide")

# Carregamento e preparação dos dados
# Lê o arquivo CSV contendo as vendas do supermercado, com delimitador ";" e decimais separados por ","
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")

# Converte a coluna "Date" para o formato datetime para facilitar manipulações baseadas em datas
df["Date"] = pd.to_datetime(df["Date"])

# Ordena os dados pela coluna "Date" para manter uma sequência cronológica
df = df.sort_values("Date")

# Cria uma nova coluna "Month" no formato "YYYY-MM" para agrupar os dados mensalmente
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

# Adiciona um seletor na barra lateral para que o usuário escolha o mês desejado para análise
month = st.sidebar.selectbox("Mês", df["Month"].unique())

# Filtra os dados de acordo com o mês selecionado pelo usuário
df_filtered = df[df["Month"] == month]

# Define o layout das colunas para exibição dos gráficos
col1, col2 = st.columns(2)
col3, col4, col5 = st.columns(3)

# Gráfico 1: Faturamento por dia com separação por filial
# Mostra o total de vendas por dia, agrupado por cidade
fig_date = px.bar(
    df_filtered, x="Date", y="Total", color="City", title="Faturamento por dia"
)
col1.plotly_chart(fig_date, use_container_width=True)

# Gráfico 2: Faturamento por tipo de produto
# Exibe o faturamento para cada linha de produto, agrupado por cidade
fig_prod = px.bar(
    df_filtered,
    x="Date",
    y="Product line",
    color="City",
    title="Faturamento por tipo de produto",
    orientation="h",
)
col2.plotly_chart(fig_prod, use_container_width=True)

# Gráfico 3: Faturamento total por filial
# Agrupa os dados por cidade e soma o total de vendas para cada uma
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
fig_city = px.bar(city_total, x="City", y="Total", title="Faturamento por filial")
col3.plotly_chart(fig_city, use_container_width=True)

# Gráfico 4: Distribuição do faturamento por tipo de pagamento
# Cria um gráfico de pizza para visualizar as contribuições dos diferentes métodos de pagamento
fig_kind = px.pie(
    df_filtered,
    values="Total",
    names="Payment",
    title="Faturamento por tipo de pagamento",
)
col4.plotly_chart(fig_kind, use_container_width=True)

# Gráfico 5: Média das avaliações por filial
# Calcula a média das notas de avaliação para cada cidade
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
fig_rating = px.bar(
    city_rating, y="Rating", x="City", title="Média de avaliação por filial"
)
col5.plotly_chart(fig_rating, use_container_width=True)
