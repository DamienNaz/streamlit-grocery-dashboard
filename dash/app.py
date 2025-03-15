import streamlit as st

import plotly.express as px
import pandas as pd
from millify import millify
from streamlit_extras.metric_cards import style_metric_cards
import plotly.graph_objects as go

st.set_page_config(page_title="Grocery", page_icon=':green_apple:', layout="wide", initial_sidebar_state='expanded')
from pages import first_page, second_page, third_page  

data = pd.read_csv('./dataset/grocery_final.csv')
labels = {'Under 25': 'Menos de 25', '65+': 'Mais de 65', '25-34': 'Entre 25 e 34', '45-54': 'Entre 45 e 54',
          '35-44': 'Entre 35 e 44', '55-64': 'Entre 55 e 64'}
data['household_age'] = data['household_age'].map(labels)

custom_order = ['Menos de 25', 'Entre 25 e 34', 'Entre 35 e 44', 'Entre 45 e 54', 'Entre 55 e 64', 'Mais de 65']
data_1 = pd.DataFrame({'Age': custom_order})
mapping = {age: i for i, age in enumerate(custom_order)}
data['order'] = data['household_age'].map(mapping)

data_sorted = data.sort_values(by='order')
data_sorted.drop(columns=['order'], inplace=True)
data_sorted.reset_index()

def grafico_8(data_sorted):
    top_product_sales = data_sorted.groupby('product_type')['sales_value'].sum().nlargest(10).reset_index()

    figura = px.bar(top_product_sales, x='sales_value', y='product_type', orientation='h', title='Top 10 - Produtos mais vendidos',
                 labels={'sales_value': 'Vendas', 'product_type': 'Produtos'},
                 category_orders={'product_type': top_product_sales['product_type'].tolist()})

    top_product_sales.sort_values('sales_value', ascending=False, inplace=True)

    figura.update_traces(marker_color='#9FC131')
    figura.update_layout(plot_bgcolor='white', title_x=0.295)
    figura.update_xaxes(title_text='Total Vendas',  gridcolor='lightgray')
    figura.update_yaxes(title_text='Produtos',  gridcolor='lightgray')
    figura.update_yaxes(showgrid=False, categoryorder='total ascending',gridwidth=0.1, gridcolor='lightgrey', griddash='dot', ticks='outside')

    return figura

def grafico_9(data_sorted):
    top_product_sales = data_sorted.groupby('product_department')['sales_value'].sum().nlargest(11).reset_index()

    figura = px.bar(top_product_sales, x='sales_value', y='product_department', orientation='h', title='Top 10 - Categoria de produtos mais vendidos',
                 labels={'sales_value': 'Vendas', 'product_department': 'Departamentos'},
                 category_orders={'product_department': top_product_sales['product_department'].tolist()})

    top_product_sales.sort_values('sales_value', ascending=False, inplace=True)

    figura.update_traces(marker_color='#9FC131')
    figura.update_layout(plot_bgcolor='white', title_x=0.24)
    figura.update_xaxes(title_text='Total Vendas',  gridcolor='lightgray')
    figura.update_yaxes(title_text='Categoria',  gridcolor='lightgray')
    figura.update_yaxes(showgrid=False, categoryorder='total ascending',gridwidth=0.1, gridcolor='lightgrey', griddash='dot', ticks='outside')

    return figura


def grafico_10(data_sorted):
    data_sorted['transaction_timestamp'] = pd.to_datetime(data_sorted['transaction_timestamp'])
    sales_by_department_month = \
    data_sorted.groupby([data_sorted['transaction_timestamp'].dt.month, 'product_department'])[
        ['quantity', 'sales_value']].sum().reset_index()
    sales_by_department_month.rename(columns={'transaction_timestamp': 'Month'}, inplace=True)

    top_3_products = sales_by_department_month.groupby('product_department')['sales_value'].sum().nlargest(3).index
    sales_by_department_month = sales_by_department_month[
        sales_by_department_month['product_department'].isin(top_3_products)]

    month_names = ['Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho', 'Julho', 'Agosto', 'Setembro', 'Outubro',
                   'Novembro', 'Dezembro']
    sales_by_department_month['Month'] = sales_by_department_month['Month'].apply(lambda x: month_names[x - 1])

    fig = px.bar(sales_by_department_month, x='Month', y='sales_value', color='product_department', width=680,
                 title='Top 3 - Evolução das três categórias de produtos mais vendidos ao longo do ano',
                 labels={'sales_value': 'Soma das Vendas', 'Month': 'Mês', 'product_department':'Categoria de produto:'},
                 barmode='stack',
                 color_discrete_map={'GROCERY': '#006769', 'MEAT': '#FF9F66', 'PRODUCE': '#9DDE8B'}
                 )
    fig.update_layout(plot_bgcolor='white', title_x=0.08)
    fig.update_layout(
        plot_bgcolor='white',
        legend=dict(
            orientation='h',
            yanchor='bottom',
            y=-0.5,
            xanchor='center',
            x=0.5,
        )
    )

    return fig

# Creates the container for page title
dash_1 = st.container()

with dash_1:
    st.markdown(
        """
        <div style='text-align: center; padding: 10px; background-color: #9DDE8B; color: white; font-size: 24px; border-radius: 10px;'>
            Grocery Store DashBoard
        </div>
        """, unsafe_allow_html=True)
    st.write("")

# Creates the container for metric card
dash_2 = st.container()

with dash_2:
    # Get KPI metrics
    total_sales = (data_sorted['quantity'] * data_sorted['sales_value']).sum()

    total_stores = len(data_sorted['store_id'].unique())

    total_orders = data_sorted['basket_id'].nunique()



    col1, col2, col3 = st.columns(3)
    # Create column span
    col1.metric(label="Vendas Anuais", value="$" + millify(total_sales, precision=2))
    col2.metric(label="N.º Lojas", value=total_stores)

    col3.metric(label="N.º Ordens", value=total_orders)

    # This is used to style the metric card
    style_metric_cards(border_left_color="#DBF227")


    dash_3 = st.container()

    with dash_3:
        col1, col2 = st.columns(2)

        grafico_8 = grafico_8(data_sorted)
        grafico_9 = grafico_9(data_sorted)
        grafico_10 = grafico_10(data_sorted)

        with col1:
            st.plotly_chart(grafico_8,use_container_width=True)

        with col2:
            st.plotly_chart(grafico_9,use_container_width=True)


    dash_4 = st.container()

    def calcular_estatisticas_cesto(data_sorted):
        cesto = data_sorted.copy()
        cesto['total_value'] = cesto['sales_value'] * cesto['quantity']
        basket_totals = cesto.groupby('basket_id')['total_value'].sum()

        average_basket_value = basket_totals.mean()
        average_basket_value_rounded = round(average_basket_value, 2)

        min_basket_value = basket_totals.min()
        max_basket_value = basket_totals.max()

        return average_basket_value_rounded, min_basket_value, max_basket_value

    with dash_4:
        col1, col2 = st.columns([1, 1])

        with col1:
            valor_medio, valor_min, valor_max = calcular_estatisticas_cesto(data_sorted)

            meta_objectivo = 45 # objectivo do valor médio
            meta_min = 30 # valor minimo
            meta = 80 # valor acima das expectativas

            value = valor_medio


            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=value,
                title={'text': "Cesto Médio"},
                number={'suffix': " $"},
                gauge={
                    'axis': {'range': [meta_min, meta]},
                    'bar': {'color': "#005C53"},
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': meta_objectivo
                    }
                }
            ))

            fig.update_layout(height=400, width=800)
            fig.add_annotation(
                x=0.25, y=0.9,
                xref='paper', yref='paper',
                text="Objetivo",
                showarrow=True,
                arrowhead=5,
                ax=-45, ay=-30,
                font=dict(size=12, color="red"),
                align="center"
            )

            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.plotly_chart(grafico_10)
