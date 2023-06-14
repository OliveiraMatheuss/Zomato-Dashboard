import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
import inflection
from folium.plugins import MarkerCluster
from millify import millify as mil
from src import transformation as ts
from src import markdown as mk

st.set_page_config(page_title= 'Cuisines',
                    layout= 'wide')


#===============================================================================================================#
#================================ CARGA DE DADOS E LIMPEZA =====================================================#
#===============================================================================================================#

df = pd.read_csv("dataset/zomato.csv")
df1 = ts.limpeza(df)

#==============================================================================================================#
#==============================================  SIDEBAR  =====================================================#
#==============================================================================================================#


st.sidebar.title("Zotomato",)
st.sidebar.markdown('## Filtros')

select_country_mult = st.sidebar.multiselect(label ='Escolha os Paises que Deseja visualizar as informações',
                                            options = df1.country_name.unique(), default= df1.country_name.sample(10).unique())
st.sidebar.divider()

select_quant_restaurant = st.sidebar.slider(label = 'Selecione a quantidade de restaurantes', 
                                            value = (1,10),
                                            max_value= 20)
st.sidebar.divider()

select_cuisines_mult = st.sidebar.multiselect(label = 'Escolha os tipos de culinária',
                                            options = df1.cuisines.unique(),
                                            default = df1.cuisines.sample(10).unique())

# filtros

df1 = df1[df1['country_name'].isin(select_country_mult)]

#==============================================================================================================#
#====================================    LAYOUT      ==========================================================#
#==============================================================================================================#