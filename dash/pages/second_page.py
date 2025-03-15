import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

#######################################Evolução Das Vendas Por Loja Ao Longo Do Ano (ScatterPlot)#########################################################
def grafico_10(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)

    df['transaction_timestamp'] = pd.to_datetime(df['transaction_timestamp'])

    df_monthly = df.groupby([df['transaction_timestamp'].dt.to_period('M'), 'store_id']).agg(
        {'sales_value': 'sum', 'quantity': 'sum'}
    ).reset_index()

    df_monthly['transaction_timestamp'] = df_monthly['transaction_timestamp'].astype(str)

    sales_value_min = df_monthly['sales_value'].min()
    sales_value_max = df_monthly['sales_value'].max()
    sales_value_range = [sales_value_min * 0.9 if sales_value_min > 0 else 0, sales_value_max]

    df_monthly['store_id'] = df_monthly['store_id'].astype(str)
    store_colors = ['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF', '#00FFFF']
    store_color_map = {store_id: color for store_id, color in zip(df_monthly['store_id'].unique(), store_colors)}

    figura_6 = px.scatter(
        df_monthly,
        x="sales_value",
        y="quantity",
        title='Evolução das vendas por loja ao longo do ano',
        animation_frame="transaction_timestamp",
        color="store_id",
        hover_name="transaction_timestamp",
        size="sales_value",
        range_x=sales_value_range,
        range_y=[0, df_monthly['quantity'].max()],
        labels={'sales_value': 'Vendas', 'quantity': 'Quantidade', 'transaction_timestamp': 'Mês', 'store_id': 'Lojas'},
        color_discrete_map=store_color_map, width=1250, height=800
    )

    figura_6.update_layout(
        plot_bgcolor='white',
        legend_orientation='h',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=0.8
        ),
        title_x=0.3
    )

    figura_6.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 900

    figura_6.update_xaxes(showgrid=True,
                          gridwidth=0.1,
                          gridcolor='lightgrey',
                          griddash='dot')

    return figura_6

    #######################################Vendas Totais Por Loja (BoxPlot)#########################################################
def grafico_4(caminho_arquivo):
    df = pd.read_csv(caminho_arquivo)

    # Cria um boxplot para cada loja
    grupo_por_loja = df.groupby('store_id')
    boxplots = []

    for i, (store_id, vendas) in enumerate(grupo_por_loja):
        boxplots.append(go.Box(y=vendas['sales_value'], name=f'Loja {store_id}', marker_color='#1f77b4'))

    layout_boxplot = go.Layout(
        title={'text': 'Vendas Totais por Loja', 'x': 0.5},
        xaxis=dict(title='ID da Loja'),
        yaxis=dict(title='Vendas Totais'),
        width=1250,
        height=800,
        template='plotly_white',
        showlegend=False
    )

    figura_3 = go.Figure(data=boxplots, layout=layout_boxplot)

    return figura_3


def app():
    st.markdown(
        """
        <div style='text-align: center; padding: 10px; background-color: #2A629A; color: white; font-size: 24px; border-radius: 10px;'>
            Lojas
        </div>
        """, unsafe_allow_html=True)
    st.write("Nesta página tiramos conclusões sobre o desempenho e as características das lojas.")

    caminho_arquivo = 'grocery_final.csv'

    # Criar os gráficos
    figura_6 = grafico_10(caminho_arquivo)
    figura_3 = grafico_4(caminho_arquivo)

    # Mostrar o gráfico de dispersão
    st.plotly_chart(figura_6)

    # Filtro para selecionar uma loja
    df = pd.read_csv(caminho_arquivo)
    lojas_disponiveis = sorted(df['store_id'].astype(str).unique())
    loja_selecionada = st.selectbox('Selecione uma loja:', options=['Todas as lojas'] + lojas_disponiveis)

    # Filtrar os boxplots de acordo com a loja selecionada
    if loja_selecionada != 'Todas as lojas':
        boxplot_selecionado = [boxplot for boxplot in figura_3.data if boxplot['name'] == f'Loja {loja_selecionada}']
        figura_3_filtrada = go.Figure(data=boxplot_selecionado, layout=figura_3.layout)
        st.plotly_chart(figura_3_filtrada)
    else:
        st.plotly_chart(figura_3)


if __name__ == "__main__":
    app()