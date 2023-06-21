import pandas as pd
import utils.cityfunc  as cityfunc 
import streamlit as st
from utils import transformation as ts
from utils import markdown as mk


st.set_page_config(page_title= 'Countries',
                    layout= 'wide')

cores_paises = {'Philippines': '#FED141',
                        'Brazil': '#009739',
                        'Australia': '#012169', 
                        'United States of America': '#B31942',
                        'Singapore': '#C73b3C',
                        'United Arab Emirates': '#000000',
                        'India': '#FF671F',
                        'England': '#CE1124',
                        'South Africa': '#007749',
                        'Sri Lanka': '#8D153A'}
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

select_country_mult = st.sidebar.multiselect(label ='Escolha os Paises que Deseja visualizar os Restaurantes',
                                                options = df1.country_name.unique(), default= df1.country_name.unique())

# filtros

df1 = df1[df1['country_name'].isin(select_country_mult)]

#==============================================================================================================#
#====================================    LAYOUT      ==========================================================#
#==============================================================================================================#


st.header('🏙️ Cidades')
 
with st.container():
    # Title
    corpo = mk.aling(h = 'h4', text= 'Top 10 Cidades com maior quantidade de restaurantes')
    st.markdown(corpo, unsafe_allow_html=True)
    
    #Grafico
    fig = cityfunc.top_restaurants(df1, cores_paises= cores_paises)
    st.plotly_chart(fig, use_container_width= True)
    
    #Separação
    st.markdown('---')

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        #title
        
        corpo = mk.aling(h = 'h4', text= 'Cidades com restaurantes avaliados acima de 4')
        st.markdown(corpo, unsafe_allow_html=True)    
        
        #Grafico

        fig = cityfunc.rest_star_higher(df1, cores_paises)
        st.plotly_chart(fig, use_container_width= True)
        
        
    with col2:
        #title
        corpo = mk.aling(h = 'h4', text= 'Cidades com restaurantes avaliados abaixo de 2.5')
        st.markdown(corpo, unsafe_allow_html=True)
        
        #plot 
        fig = cityfunc.rest_star_lower(df1, cores_paises) 
        st.plotly_chart(fig, use_container_width= True)
        
with st.container():
    st.markdown('---')  
    
    #title     
    corpo = mk.aling(h = 'h4', text= 'Top 10 Cidades com a maior quantidade de topos de culinária ')
    st.markdown(corpo, unsafe_allow_html=True)
    
    #plot
    fig = cityfunc.top_cuisines(df1, cores_paises)
    st.plotly_chart(fig, use_container_width= True)

