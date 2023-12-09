import pandas as pd
import streamlit as st
import plotly_express as px
from streamlit_extras.metric_cards import  style_metric_cards

@st.cache_data
def carregar_dados():
    df = pd.read_excel("Vendas.xlsx") 
    return df

def main():

    st.set_page_config(layout="wide", page_icon="📊")
    
    st.title("Dashboard de Vendas 📊")

    # Lendo a base de dados
    df = carregar_dados()

    ano_filtrado = st.sidebar.selectbox("Filtrar por ano",["Todos",*df["Ano"].unique()])
    # ou
    # ano_filtrado = st.sidebar.selectbox("Filtrar por ano",['Todos'].extend(df['Ano'].unique()) )

    st.sidebar.image("fariaslrc.jpg")
    
    # Aplicar filtro apenas se não for todos
    if ano_filtrado != "Todos":
        df_filtrado = df[df["Ano"] == ano_filtrado]
        # # Pegando on" + total_lucro[:2] + "." + total_lucro[2:5] + "." + total_lucro[5:]
    else:
        df_filtrado = df

    # Calcula o total do custo e formata como moeda
    total_custo = df_filtrado["Custo"].sum()
    total_custo = f"R$ {total_custo:,.2f}"

    # Calcula o total do lucro e formata como moeda
    total_lucro = df_filtrado["Lucro"].sum()
    total_lucro = f"R$ {total_lucro:,.2f}"
    

    total_clientes = df_filtrado["ID Cliente"].nunique()

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Custo", total_custo)   
        # white
        style_metric_cards(border_left_color = "#3e4095")
        # black     
        #style_metric_cards(border_left_color = "#3e4095", background_color = "#000")
    with col2:
        st.metric("Total Lucro", total_lucro)
    with col3:
        st.metric("Total Clientes", total_clientes)
    
    st.markdown(
            """
            <style>
            [data-testid="stMetricValue"] {
                font-size: 18px;
                color: rgba(0,0,0,0,)
            }
            </style>
            """,
            unsafe_allow_html=True,
            )

    # col1.metric("Total Custo", int(total_custo))
    # col2.metric("Total Lucro", int(total_lucro))
    # col3.metric("Total CLientes", int(total_clientes))

    produtos_vendidos_marca = df_filtrado.groupby("Marca")["Quantidade"].sum().sort_values(ascending=True).reset_index()
    
    lucro_categoria = df_filtrado.groupby("Categoria")["Lucro"].sum().sort_values(ascending=False).reset_index()
        
    # st.write(df.head())

    col1, col2 = st.columns(2)

    fig1 = px.bar(produtos_vendidos_marca, x='Quantidade', y='Marca', 
            orientation='h', title="Total Produtos Vendidos por Marca",
            color_discrete_sequence=['#3e4095'],
            width=500, height=350, text="Quantidade")
    fig1.update_layout(title_x = 0.3)
    fig1.update_yaxes(automargin=True)
    col1.plotly_chart(fig1)

    fig2 = px.pie(lucro_categoria, values='Lucro', names='Categoria', 
            title='Lucro por categoria', hole=.6,
            color_discrete_sequence=['#3e4095',"#EC610c"],
            width=500, height=350)
    fig2.update_layout(title_x = 0.4)
    col2.plotly_chart(fig2)


    lucro_mes_categoria = df_filtrado.groupby(["mes_ano","Categoria"])["Lucro"].sum().reset_index()

    fig = px.line(lucro_mes_categoria, x='mes_ano', y='Lucro', 
            title="Lucro x Mês x Categoria",
            #color_discrete_sequence=['#3e4095',"#EC610c","#FFFFFF"],
            color="Categoria", markers=True)
    fig.update_layout(title_x = 0.3)
    st.plotly_chart(fig)

if __name__ == '__main__':
    main()
