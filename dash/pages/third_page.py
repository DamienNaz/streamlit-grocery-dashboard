import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Vendas",page_icon=':green_apple:',layout="wide",initial_sidebar_state='expanded')
caminho_arquivo = 'grocery_final.csv'
dados = pd.read_csv(caminho_arquivo)


#######################################Vendas Por Departamento(gráfico de barras)#########################################################
def grafico1(dados, loja_selecionada):
    vendas_por_departamento = dados[dados['store_id'] == loja_selecionada].groupby('product_department')['sales_value'].sum().reset_index()

    colors = ['lightgray' for i in range(len(vendas_por_departamento))]

    figura = px.bar(vendas_por_departamento, y='product_department', x='sales_value',
                 color = 'product_department',
                 labels={'sales_value': 'Vendas', 'product_department': 'Departamentos'},
                 color_discrete_sequence= colors,
                 color_discrete_map={'GROCERY': '#6895D2'},
                 height=450, width=700)

    figura.update_layout(plot_bgcolor='white', showlegend=False)

    figura.update_yaxes(categoryorder='total ascending')

    figura.update_yaxes(labelalias={'PASTRY': 'Padaria', 'GROCERY': 'Mercearia', 'DELI': 'Congelados',
                                   'PRODUCE': 'Produtos Frescos', 'MEAT': 'Carnes', 'SEAFOOD': 'Frutos do Mar',
                                   'COSMETICS': 'Cosméticos', 'NUTRITION': 'Nutrição', 'SPIRITS': 'Bebidas Alcoólicas'})
    return figura

#######################################Evolução das vendas totais por loja (grafico de linhas)#########################################################
def grafico2(dados, loja_selecionada):
    dados['data'] = pd.to_datetime(dados['transaction_timestamp']).dt.to_period('M')

    # Agrupa por loja e mês e calcula a soma de 'sales_value'
    vendas_por_loja = dados[dados['store_id'] == loja_selecionada].groupby(['store_id', 'data'])['sales_value'].sum().reset_index()

    # Converte a coluna 'data' para string com o nome do mês
    vendas_por_loja['data'] = vendas_por_loja['data'].dt.strftime('%b')

    # Cria uma lista de meses para garantir que todos os meses estejam presentes no eixo X
    meses = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    vendas_por_loja = vendas_por_loja.set_index('data').reindex(meses).reset_index()
    vendas_por_loja = vendas_por_loja.fillna(0)

    figura = px.line(vendas_por_loja, x='data', y='sales_value',
                     labels={'data': 'Mês', 'sales_value': 'Vendas'},
                     color_discrete_sequence=["#6895D2"])

    figura.update_yaxes(range=[1000, 7000])

    figura.update_layout(plot_bgcolor='white')

    figura.update_xaxes(categoryorder='array', categoryarray=meses)

    return figura

#######################################Vendas De Produtos Por Faixas Etárias(gráfico de barras)#########################################################
def grafico3(dados, faixas_etarias_escolhidas):
    dados_filtrados = dados[dados['household_age'].isin(faixas_etarias_escolhidas)]
    contagem_produtos = dados_filtrados.groupby(['household_age', 'product_department']).size().unstack(fill_value=0)
    vendas_por_departamento = contagem_produtos.reset_index().melt(id_vars='household_age', var_name='product_department', value_name='sales_value')
    figura = px.bar(vendas_por_departamento,
                   y='sales_value',
                   x='product_department',
                   color='household_age',
                   barmode='group',
                   labels={'sales_value': 'Vendas', 'product_department': 'Departamento', 'household_age': 'Faixa Etária'},
                   color_discrete_map={'25-34': '#FFA62F', '55-64': '#ACD793'},
                   height=450, width=1100)

    figura.update_layout(plot_bgcolor='white')
    figura.update_yaxes(categoryorder='total ascending')
    figura.update_xaxes(labelalias={'PASTRY': 'Padaria', 'GROCERY': 'Mercearia', 'DELI': 'Congelados',
                                   'PRODUCE': 'Produtos Frescos', 'MEAT': 'Carnes', 'SEAFOOD': 'Frutos do Mar',
                                   'COSMETICS': 'Cosméticos', 'NUTRITION': 'Nutrição', 'SPIRITS': 'Bebidas Alcoólicas'})
    return figura

def app():
    st.markdown(
        """
        <div style='text-align: center; padding: 10px; background-color: #2A629A; color: white; font-size: 24px; border-radius: 10px;'>
            Vendas
        </div>
        """, unsafe_allow_html=True)
    st.write("Nesta página podemos analisar e tirar conclusões sobre o desempenho e as tendências das vendas.")

    lojas = dados['store_id'].unique()
    loja_selecionada = st.selectbox('Selecione uma loja', lojas)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(f"Vendas por Departamento na Loja {loja_selecionada}")
        figura1 = grafico1(dados, loja_selecionada)
        st.plotly_chart(figura1, use_container_width=True)

    with col2:
        st.subheader(f"Evolução das Vendas na Loja {loja_selecionada}")
        figura2 = grafico2(dados, loja_selecionada)
        st.plotly_chart(figura2, use_container_width=True)


    st.subheader("Vendas de Produtos por Faixas Etárias")
    with st.container():
        faixas_etarias = dados['household_age'].unique()
        faixas_etarias_escolhidas = st.multiselect('Selecione as faixas etárias para comparar', faixas_etarias,
                                                   default=faixas_etarias[:2])
        figura3 = grafico3(dados, faixas_etarias_escolhidas)
        st.plotly_chart(figura3, use_container_width=True)



if __name__ == "__main__":
    app()
