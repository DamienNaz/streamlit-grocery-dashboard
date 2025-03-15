import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Clientes",page_icon=':green_apple:',layout="wide",initial_sidebar_state='expanded')

df = pd.read_csv('grocery_final.csv')
caminho_arquivo = 'grocery_final.csv'
dados = pd.read_csv(caminho_arquivo)

regression = dados.copy()
regression['household_size'] = regression['household_size'].str.replace('+', '').astype(int)
regression['household_size'].unique()
regression['household_income'].unique()

def preparar_dados(dados):
    rotulos = {
        'Under 25': 'Menos de 25',
        '65+': 'Mais de 65',
        '25-34': 'Entre 25 e 34',
        '45-54': 'Entre 45 e 54',
        '35-44': 'Entre 35 e 44',
        '55-64': 'Entre 55 e 64'
    }
    dados['household_age'] = dados['household_age'].map(rotulos)

    # Ordem para classificação
    ordem_personalizada = ['Menos de 25', 'Entre 25 e 34', 'Entre 35 e 44', 'Entre 45 e 54', 'Entre 55 e 64', 'Mais de 65']
    mapeamento = {idade: i for i, idade in enumerate(ordem_personalizada)}
    dados['ordem'] = dados['household_age'].map(mapeamento)

    # Ordenar dados pela ordem_personalizada
    dados_ordenados = dados.sort_values(by='ordem')
    dados_ordenados.drop(columns=['ordem'], inplace=True)
    dados_ordenados.reset_index(drop=True, inplace=True)

    # Obter contagem de cada grupo etário
    contagem = dados_ordenados['household_age'].value_counts()
    contagem_ordem_personalizada = contagem.reindex(ordem_personalizada)

    # Preparar dados para o gráfico de barras
    contagem_df = contagem_ordem_personalizada.to_frame().reset_index()
    contagem_df.columns = ['Faixa Etária', 'Contagem']

    return contagem_df

#######################################Contagem(percentagem) das Faixas Etárias Dos Clientes (gráfico circular)#########################################################
def grafico_12(contagem_df):
    ordem_personalizada = ['Menos de 25', 'Entre 25 e 34', 'Entre 35 e 44', 'Entre 45 e 54', 'Entre 55 e 64', 'Mais de 65']
    figura_1 = px.pie(
        contagem_df,
        names='Faixa Etária',
        values='Contagem',
        category_orders={"Faixa Etária": ordem_personalizada},
        hole=0.6,
        color_discrete_sequence=px.colors.sequential.Darkmint_r
    )

    figura_1.update_layout(
        title="% das faixas etárias dos clientes",
        width=600,
        title_x=0.20,
        title_font=dict(size=18, family="Gill Sans"),
        legend=dict(
            title="Faixas Etárias",
            title_font=dict(size=14),
            font=dict(size=12),
            orientation="v"
        )
    )
    figura_1.update_traces(rotation=65)

    return figura_1

#######################################Ocorrências Por Intervalos De Rendimentos (gráfico de barras)#########################################################
def grafico_13(regression):
    specific_order = ['Under 25K', '25-49K', '50-74K', '75-99K', '100-124K', '125-149K', '150-174K', '175-199K', '200K+']
    regression_sorted = regression['household_income'].value_counts().reindex(specific_order)

    color_palette = ['#377683', '#065465', '#065465', '#065465', '#065465', '#065465', '#065465', '#065465', '#065465']
    figura_3 = px.bar(
        x=regression_sorted.values,
        y=regression_sorted.index,
        orientation='h',
        width=600,
        height=500,
        color_discrete_sequence=color_palette,
    )

    max_value = regression_sorted.max()
    figura_3.add_shape(
        type='line',
        x0=max_value,
        y0=0,
        x1=max_value,
        y1=len(specific_order),
        line=dict(color='grey', width=2, dash='dash'),
        xref='x',
        yref='y'
    )

    figura_3.update_layout(
        title='N.º de ocorrências por Intervalos de Rendimentos',
        xaxis=dict(title='Número de ocorrências'),
        yaxis=dict(title='Intervalos de Rendimentos'),
        title_x=0.15,
        title_font=dict(size=18, family="Gill Sans"),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )

    return figura_3

#######################################Transações por Hora do dia (histograma)#########################################################
def grafico_7(df):
    df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'])
    df['hour'] = df['transaction_timestamp'].dt.hour

    st.sidebar.title('Filtro Histograma')
    start_hour = st.sidebar.slider('Hora de Início', min_value=8, max_value=22, value=8)
    end_hour = st.sidebar.slider('Hora de Fim', min_value=8, max_value=22, value=22)

    filtered_df = df[(df['hour'] >= start_hour) & (df['hour'] <= end_hour)]

    figura_4 = px.histogram(filtered_df, x='hour', title='Transações por Hora do Dia',
                            labels={'hour': 'Hora do Dia', 'count': 'Ocorrências'},
                            nbins=min(end_hour - start_hour + 1, 24), color_discrete_sequence=['#9AD0C2'])

    figura_4.update_layout(plot_bgcolor='rgba(0,0,0,0)',
                           paper_bgcolor='rgba(0,0,0,0)',
                           width=1250,
                           height=500,
                           title_x=0.38)

    return figura_4
def app():
    contagem_df = preparar_dados(dados)
    st.markdown(
        """
        <div style='text-align: center; padding: 10px; background-color: #2A629A; color: white; font-size: 24px; border-radius: 10px;'>
            Clientes
        </div>
        """, unsafe_allow_html=True)
    st.write("Nesta página podemos analisar e tirar conclusões relativamente ao comportamento e às preferências dos clientes.")

    figura_3 = grafico_13(regression)
    col1, col2 = st.columns(2)
    with col1:
        figura_1 = grafico_12(contagem_df)
        st.plotly_chart(figura_1)
    with col2:
        st.plotly_chart(figura_3)

    with st.container():
        st.plotly_chart(grafico_7(df))

if __name__ == "__main__":
    app()
