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

select_country_mult = st.sidebar.multiselect(label ='Escolha os Paises que Deseja visualizar os Restaurantes',
                                                options = df1.country_name.unique(), default= df1.country_name.unique())

# filtros

df1 = df1[df1['country_name'].isin(select_country_mult)]

#==============================================================================================================#
#====================================    LAYOUT      ==========================================================#
#==============================================================================================================#


st.header('🏙️ Cidades')

with st.container():

    corpo = mk.aling(h = 'h4', text= 'Top 10 Cidades com maior quantidade de restaurantes')
    st.markdown(corpo, unsafe_allow_html=True)
    
    cols = ['restaurant_id', 'city', 'country_name']
    aux = df1.loc[:,cols].groupby(['country_name','city']).count().sort_values(by = 'restaurant_id', ascending= False).reset_index().head(10)
    bar = px.bar(aux, x = 'city', y = 'restaurant_id', 
        labels= {
            'city': 'Cidade',
            'restaurant_id':  'Qte de restaurantes',
            'country_name': 'Pais'}
        )
    st.plotly_chart(bar, use_container_width= True)
    st.divider()       
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        corpo = mk.aling(h = 'h4', text= 'Cidades com restaurantes avaliados acima de 4')
        st.markdown(corpo, unsafe_allow_html=True)    
        
        cols = ['city','restaurant_id', 'country_name']
        aux = df1[df1['aggregate_rating'] > 4]
        aux = aux.loc[:,cols].groupby(['country_name','city']).count().sort_values(by = 'restaurant_id', ascending= False).reset_index().head(10)
        bar = px.bar(aux, x = 'city', y = 'restaurant_id', 
                labels={
                    'city': 'Cidade',
                    'restaurant_id':'Quantidade de Restaurantes',
                    'country_name':'Pais'
                }) 
        st.plotly_chart(bar, use_container_width= True)
        
        
    with col2:
        
        corpo = mk.aling(h = 'h4', text= 'Cidades com restaurantes avaliados abaixo de 2.5')
        st.markdown(corpo, unsafe_allow_html=True)
        
        cols = ['city','restaurant_id', 'country_name']
        aux = df1[df1['aggregate_rating'] <= 2.5]
        aux = aux.loc[:,cols].groupby(['country_name','city']).count().sort_values(by = 'restaurant_id', ascending= False).reset_index().head(15)
        aux.columns = ['country_name','city', 'num_restaurantes']

        bar = px.bar(aux, x = 'city', y = 'num_restaurantes', 
                labels={
                    'city': 'Cidade',
                    'num_restaurantes':'Quantidade de Restaurantes',
                    'country_name':'Pais'
                })
        st.plotly_chart(bar, use_container_width= True)
        
with st.container():
    st.divider()      
    corpo = mk.aling(h = 'h4', text= 'Top 10 Cidades com a maior quantidade de topos de culinária ')
    st.markdown(corpo, unsafe_allow_html=True)
    
    cols = ['city', 'cuisines', 'country_name']
    aux = df1[cols].groupby(['city', 'country_name']).nunique().sort_values(by='cuisines', ascending=False).reset_index().head(10)
    bar = px.bar(aux, x='city', y='cuisines')

    st.plotly_chart(bar, use_container_width= True)

