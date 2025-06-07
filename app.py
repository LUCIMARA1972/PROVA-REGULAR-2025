import streamlit as st
import pandas as pd
import plotly.express as px

# Codigo atualizado corretamente
df = pd.read_csv('bases_upload/tabela1_obitos_por_estado.csv', sep=',')
df = df.drop(columns=['UF'])
             
colunas_alvo = ['ignorado','vivo','obito']
for col in colunas_alvo:
    df[col] = pd.to_numeric(df[col], errors = 'coerce')

st.title('Analise de Dados - Febre Amarela - 30 anos')
st.write('Visualização da Tabela:')
st.dataframe(df)

st.subheader('Análise de nulos')
nulos = df.isnull().sum()
st.dataframe(nulos)

aux = pd.DataFrame({'variavel': nulos.index, 'qtd_miss':nulos.values})
st.dataframe(aux)

st.subheader('Análises univariadas')
st.write('Medidas resumo')
st.dataframe(df.describe())

coluna_escolhida = st.selectbox('Escolha a coluna para analise:', df.columns)

df.loc[df[coluna_escolhida] >999, coluna_escolhida] = 999
df.loc[df[coluna_escolhida] <0, coluna_escolhida] = 100

lista_de_colunas = df.columns
coluna_escolhida = st.selectbox('selecione a coluna',lista_de_colunas)
media = round(df[coluna_escolhida].mean(),2)
desvio = round(df[coluna_escolhida].std(),2)
mediana = round(df[coluna_escolhida].quantile(0.5),2)
maximo = round(df[coluna_escolhida].max(),2)

st.write(f'A coluna escolhida foi {coluna_escolhida}. Média = {media}. Desvio = {desvio}. Mediana = {mediana} e Máximo = {maximo}')
st.write('Histograma')
fig = px.histogram(df,x='ignorado')
st.plotly_chart(fig)
st.write('Boxplot')
fig2 = px.box(df,x='ignorado')
st.plotly_chart(fig2)

st.subheader('Análises Multivariadas')
lista_de_escolha = st.multiselect('Escolha até 3 variaveis:',['ignorado', 'obito', 'vivo'])
st.markdown('Gráfico de dispersão')
if len(lista_de_escolha) != 3:
    st.warning('Selecione exatamente 3 colunas para gerar os gráficos.')
else:
    fig3 = px.scatter(df, x=lista_de_escolha[0], y=lista_de_escolha[1], color=lista_de_escolha[2])
    st.plotly_chart(fig3)

    st.markdown('Gráfico de Caixa')
    fig4 = px.box(df, x=lista_de_escolha[0], y=lista_de_escolha[1], color=lista_de_escolha[2])
    st.plotly_chart(fig4)   

col1, col2 = st.columns(2)
with col1:
    st.subheader('Histograma')
    fig = px.histogram(df, x=coluna_escolhida)
    st.plotly_chart(fig, use_container_width=True, key = 'histograma')
with col1:
    st.subheader('Boxplot')
    fig2 = px.box(df, x=coluna_escolhida)
    st.plotly_chart(fig, use_container_width=True, key = 'boxplot')

    media = round(df[coluna_escolhida].mean(), 2)
mediana = round(df[coluna_escolhida].median(), 2)
desvio = round(df[coluna_escolhida].std(), 2)
maximo = round(df[coluna_escolhida].max(), 2)
minimo = round(df[coluna_escolhida].min(), 2)

st.markdown(f"""
### Resumo Estatístico da Coluna *{coluna_escolhida}*

- *Média:* {media}  
- *Mediana:* {mediana}  
- *Desvio Padrão:* {desvio}  
- *Valor Máximo:* {maximo}  
- *Valor Mínimo:* {minimo}

Esses valores representam o comportamento dos dados da coluna escolhida.  
Os valores apresentados sintetizam as principais medidas descritivas da coluna escolhida para ser analisada. A média e a mediana indicam a tendencia central, enquanto o desvio padrão e o intervalo caracterizam a dispesão dos dados. A análise gráfica facilita a identificação de padrões, distribuição dos dados e possiveis outliers, auxiliando na internpretação estatística e na compreensão da variabilidade da amostra.""")

