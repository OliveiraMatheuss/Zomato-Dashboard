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
    corpo = mk.aling(h = 'h4', text= 'Quantidade de Restaurante por Pais')
    st.markdown(corpo, unsafe_allow_html=True)
    cols = ['country_name', 'restaurant_id']
    aux = df1.loc[:,cols].groupby('country_name').count().sort_values( by= 'restaurant_id',ascending=False).head(10).reset_index().head()
    bar = px.bar(aux, x = 'country_name', y = 'restaurant_id',
            labels= {
                'country_name': 'Pais',
                'restaurant_id': 'Qtd de Restaurantes'
            }
            )
    st.plotly_chart(bar, use_container_width= True)
    
with st.container():
    corpo = mk.aling(h = 'h4', text = 'Quantidade de Cidades por Pais')
    st.markdown(corpo, unsafe_allow_html= True)    
    
    cols = ['country_name','city','restaurant_id']
    aux = df1.loc[:,cols].groupby(['country_name', 'city']).count().reset_index()
    aux = aux.loc[:,['country_name', 'city']].groupby('country_name').count().sort_values(by = 'city',ascending=False).reset_index().head()
    bar = px.bar(aux, x = 'country_name', y = 'city',
                labels={
                    'country_name' : 'Pais',
                    'city': 'Qtd de Cidades'
                })
    st.plotly_chart(bar, use_container_width= True)

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        corpo = mk.aling('h5', text= 'Quantidade de Avaliações feitas por Pais')
        st.markdown(corpo, unsafe_allow_html= True)
        cols = ['country_name','votes']
        aux = df1.loc[:,cols].groupby('country_name').mean().sort_values(by = 'votes', ascending= False).reset_index().head(5)
        bar = px.bar(aux, x = 'country_name', y = 'votes',
                labels= {
                    'country_name': 'Pais',
                    'votes': 'Quantidade de Avaliações'
                }) 
        st.plotly_chart(bar, use_container_width= True)
        
    with col2:
        corpo = mk.aling(h = 'h5', text= 'Média de Preço por um prato para duas pessoas')
        st.markdown(corpo, unsafe_allow_html= True)
        cols = ['country_name', 'average_cost_for_two']
        aux = df1[cols].groupby('country_name').mean('average_cost_for_two')
        aux = aux.reset_index()
        aux = aux.sort_values(by = 'average_cost_for_two', ascending= False).head()
        bar = px.bar(aux, x = 'country_name', y = 'average_cost_for_two', 
                labels ={
                        'country_name': 'Pais',
                        'average_cost_for_two': 'Preço Médio'
                } )
        st.plotly_chart(bar, use_container_width= True)