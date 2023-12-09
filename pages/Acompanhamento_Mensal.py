import pandas as pd
import streamlit as st
import plotly_express as px
from streamlit_extras.metric_cards import  style_metric_cards


@st.cache_data
def carregar_dados():
    df = pd.read_excel("Vendas.xlsx") 
    return df

def color_negative(valor):
    color = "red" if valor < 0 else "black"

    return f'color: {color}'

def main():
    st.set_page_config(layout="wide", page_icon="📊")

    st.sidebar.image("fariaslrc.jpg")

    df = carregar_dados()

    MoM = df.groupby(["mes_ano","Categoria"])["Lucro"].sum().reset_index()
    MoM["LM"] = MoM["Lucro"].shift(1)
    MoM["Variação"] = MoM["Lucro"] - MoM["LM"]
    MoM["Variação%"] = MoM["Variação"] / MoM["LM"] * 100
    MoM["Variação%"] = MoM["Variação%"].map('{:.2f}%'.format)
    MoM["Variação%"] = MoM["Variação%"].replace("nan%","")

    st.header("Análise Mensal 📆")
    df_styled = MoM.style.format({"LM": "R${:.2f}",
                                 "Lucro": "R${:.2f}",
                                 "Variação":"{:20,.2f}"})\
                                    .hide(axis="index")\
                                    .applymap(color_negative, subset=["Variação"])
    


    st.write(df_styled)


if __name__ == '__main__':
    main()