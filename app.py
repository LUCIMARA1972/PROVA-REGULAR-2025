import streamlit as st
import pandas as pd
import plotly.express as px

# Codigo atualizado corretamente
df = pd.read_csv('bases_upload/tabela1_obitos_por_estado.csv', sep=',')
df_ranking = df.copy()
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
coluna_escolhida = st.selectbox('selecione a coluna', df.columns)
st.write("Dados da coluna selecionada:")
st.write(df[coluna_escolhida])
media = round(df[coluna_escolhida].dropna().mean(),2)
desvio = round(df[coluna_escolhida].dropna().std(),2)
mediana = round(df[coluna_escolhida].dropna().quantile(0.5),2)
maximo = round(df[coluna_escolhida].dropna().max(),2)
minimo = round(df[coluna_escolhida].dropna().min(),2)

st.write(f'A coluna escolhida foi {coluna_escolhida}. Média = {media}. Desvio = {desvio}. Mediana = {mediana}. Máximo = {maximo} e Mínimo = {minimo}')
st.write('Histograma')
fig = px.histogram(df,x=coluna_escolhida)
st.plotly_chart(fig)
st.write('Boxplot')
fig2 = px.box(df,x=coluna_escolhida)
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
Os valores apresentados sintetizam as principais medidas descritivas da coluna escolhida para ser analisada. A média e a mediana indicam a tendencia central, enquanto o desvio padrão e o intervalo caracterizam a dispersão dos dados. A análise gráfica facilita a identificação de padrões, distribuição dos dados e possiveis outliers, auxiliando na interpretação estatística e na compreensão da variabilidade da amostra.""")


q1 = df[coluna_escolhida].quantile(0.25)
q3 = df[coluna_escolhida].quantile(0.75)
iqr = q3 - q1

limite_inferior = q1 - 1.5 * iqr
limite_superior = q3 + 1.5 * iqr

outliers = df[(df[coluna_escolhida] < limite_inferior) | (df[coluna_escolhida] > limite_superior)]

quantidade_outliers = outliers.shape[0]

st.write(f"Quantidade de outliers detectados na coluna *{coluna_escolhida}: **{quantidade_outliers}*")
st.write(f"Limites para detecção de outliers: Inferior = {limite_inferior:.2f}, Superior = {limite_superior:.2f}")

st.dataframe(outliers)

if coluna_escolhida.lower() == 'ignorado':
    st.subheader(f"""
*Análise da variável {coluna_escolhida}:*  
A variável {coluna_escolhida} representa os registros de casos sem desfecho informado no sistema.  
Esses dados são inseridos manualmente e indicam a ausência de informações sobre a evolução clínica dos indivíduos afetados, comprometendo a qualidade da vigilância epidemiológica.  
Altos valores nesta variável sugerem falhas no encerramento adequado dos casos, podendo indicar problemas de subnotificação ou baixa qualidade dos registros, impactando diretamente a análise dos dados de morbidade e mortalidade pela Febre Amarela.
""")

elif coluna_escolhida.lower() == 'vivo':
    st.subheader(f"""
*Análise da variável {coluna_escolhida}:*  
A variável {coluna_escolhida} refere-se aos casos com evolução favorável.  
A alta proporção de casos classificados como vivos indica eficiência no atendimento clínico e possíveis avanços nas medidas de prevenção, diagnóstico e tratamento da Febre Amarela no período analisado.
""")

elif coluna_escolhida.lower() == 'obito':
    st.subheader(f"""
*Análise da variável {coluna_escolhida}:*  
A variável {coluna_escolhida} representa o número de óbitos registrados.  
Este indicador é fundamental para mensurar a gravidade da doença e avaliar a efetividade das políticas públicas de controle e vacinação.  
O monitoramento dessa variável permite a identificação de áreas com maior letalidade e a priorização de ações de saúde pública.
""")
   
if 'ignorado' in coluna_escolhida.lower():
    ranking_UF = df_ranking.groupby('UF')['ignorado'].sum().sort_values(ascending=False).head(10)
    st.subheader("Top 3 UF com mais casos sem desfecho")
    st.dataframe(ranking_UF)

    top3 = ranking_UF.head(3)

    comentario_top3 = f"""Os estados com maior número de registros sem desfecho é: NUMERO 1 = {top3.index[0]} com {top3.iloc[0]} casos, 
NUMERO 2 = {top3.index[1]} com {top3.iloc[1]} casos e NUMERO 3 = {top3.index[2]} com {top3.iloc[2]} casos.
Esses estados podem indicar maiores dificuldades na finalização dos casos notificados, sinalizando a necessidade de melhorias nos processos de vigilancia epidemiologica local."""
    
    st.markdown(comentario_top3)


