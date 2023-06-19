import pandas as pd
import utils.countryfunc as countryfunc
import streamlit as st
from utils import transformation as ts
from utils import markdown as mk



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


st.sidebar.title("Zomato",)
st.sidebar.markdown('## Filtros')

select_country_mult = st.sidebar.multiselect(label ='Escolha os Paises que Deseja visualizar os Restaurantes', options = df1.country_name.unique(), default= df1.country_name.unique())

# filtros

df1 = df1[df1['country_name'].isin(select_country_mult)]

#==============================================================================================================#
#====================================    LAYOUT      ==========================================================#
#==============================================================================================================#

st.header('🌎 Visão Paises')

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        #title
        corpo = mk.aling(h = 'h4', text= 'Quantidade de Restaurante por Pais')
        st.markdown(corpo, unsafe_allow_html=True)
        
        #plot
        fig = countryfunc.restaurants(df1)
        st.plotly_chart(fig, use_container_width= True)
    
    with col2:
        #title
        corpo = mk.aling(h = 'h4', text = 'Quantidade de Cidades Avaliadas por Pais')
        st.markdown(corpo, unsafe_allow_html= True)    
        
        #plot
        fig = countryfunc.city(df1)
        st.plotly_chart(fig, use_container_width= True)

with st.container():
        col1, col2 = st.columns(2)
    
        with col1:
        
                #title
                corpo = mk.aling('h5', text= 'Quantidade de Avaliações feitas por Pais')
                st.markdown(corpo, unsafe_allow_html= True)
                
                #plot
                
                fig = countryfunc.votes(df1)
                st.plotly_chart(fig, use_container_width= True)
        
        with col2:
                #title
                corpo = mk.aling(h = 'h5', text= 'Média de Preço por um prato para duas pessoas')
                st.markdown(corpo, unsafe_allow_html= True)
                
                #plot
                fig = countryfunc.price(df1)
                st.plotly_chart(fig, use_container_width= True)
        
with st.container(): 

        #title
        corpo = mk.aling('h5', text = 'Paises com a maior Avaliação Média')
        st.markdown(corpo, unsafe_allow_html= True)
        
        #plot
        fig = countryfunc.aggregate_rating_higher(df1)
        st.plotly_chart(fig, use_container_width= True) 

with st.container():
        #title
        corpo = mk.aling('h5', text = 'Paises com a menor Avaliação Média')
        st.markdown(corpo, unsafe_allow_html= True)
    
        fig = countryfunc.aggregate_rating_lower(df1)
        st.plotly_chart(fig, use_container_width= True)