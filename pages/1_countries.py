import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
import inflection
from folium.plugins import MarkerCluster
from millify import millify as mil
from src import transformation as ts

st.set_page_config(page_title= 'Home',
                    layout= 'wide')


#===============================================================================================================#
#================================ CARGA DE DADOS E LIMPEZA =====================================================#
#===============================================================================================================#

df = pd.read_csv("dataset/zomato.csv")
df1 = ts.limpeza(df)

#==============================================================================================================#
#==============================================  SIDEBAR  =====================================================#
#==============================================================================================================#


st.sidebar.title("Fome Zero",)
st.sidebar.markdown('## Filtros')

select_country_mult = st.sidebar.multiselect(label ='Escolha os Paises que Deseja visualizar os Restaurantes', options = df1.country_name.unique(), default= df1.country_name.unique())

# filtros

select_country = df1[df1['country_name'].isin(select_country_mult)]