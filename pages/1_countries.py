import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
import inflection
from folium.plugins import MarkerCluster
from millify import millify as mil
from src import transformation as ts

st.set_page_config(page_title= 'Countries',
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

#==============================================================================================================#
#====================================    LAYOUT      ==========================================================#
#==============================================================================================================#

st.header('🌎 Visão Paises')

with st.container():
    st.markdown("<h3 style='text-align: center'> Quantidade de Restaurantes por Pais </h3>", unsafe_allow_html=True)
    cols = ['country_name', 'restaurant_id']
    aux = df1.loc[:,cols].groupby('country_name').count().sort_values( by= 'restaurant_id',ascending=False).head(10).reset_index().head()
    bar = px.bar(aux, x = 'country_name', y = 'restaurant_id',
            labels= {
                'country_name': 'Pais',
                'restaurant_id': 'Qtd de Restaurantes'
            }
            )
    st.plotly_chart(bar, use_container_width= True)