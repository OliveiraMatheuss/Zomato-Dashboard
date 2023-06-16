import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
import inflection
from folium.plugins import MarkerCluster
from millify import millify as mil
from src.transformation import metric_cuisine, limpeza
from src import markdown as mk

st.set_page_config(page_title= 'Cuisines',
                    layout= 'wide')


#===============================================================================================================#
#================================ CARGA DE DADOS E LIMPEZA =====================================================#
#===============================================================================================================#

df = pd.read_csv("dataset/zomato.csv")
df1 = limpeza(df)

#==============================================================================================================#
#==============================================  SIDEBAR  =====================================================#
#==============================================================================================================#


st.sidebar.title("Zotomato",)
st.sidebar.markdown('## Filtros')

select_country_mult = st.sidebar.multiselect(label ='Escolha os Paises que Deseja visualizar as informações',
                                            options = df1.country_name.unique(), default= df1.country_name.unique())
st.sidebar.divider()

select_quant_restaurant = st.sidebar.slider(label = 'Selecione a quantidade de restaurantes', 
                                            value = (10),
                                            max_value= 20)
st.sidebar.divider()

select_cuisines_mult = st.sidebar.multiselect(label = 'Escolha os tipos de culinária',
                                            options = df1.cuisines.unique(),
                                            default = ['Italian','American','Arabian','Japanese','Brazilian'])

# filtros

df1 = df1[df1['country_name'].isin(select_country_mult)]

#==============================================================================================================#
#====================================    LAYOUT      ==========================================================#
#==============================================================================================================#

with st.container():
    st.title('Melhores Restaurantes dos Principais tipos Culinários')

    Italian, American, Arabian, Japanese, Brazilian = st.columns(5)
        
    with Italian:
        metric_cuisine(df1, 'Italian')
    with American:
        metric_cuisine(df1, 'American')
    with Arabian:
        metric_cuisine(df1, 'Arabian')
        
    with Japanese:
        metric_cuisine(df1, 'Japanese')
    with Brazilian:
        metric_cuisine(df1, 'Brazilian')
    st.divider()

with st.container():
    
    st.title(f"Top {select_quant_restaurant} Restaurantes")
    st.dataframe(df1[['restaurant_id',
                        'restaurant_name',
                        'country_name',
                        'city',
                        'cuisines',
                        'average_cost_for_two',
                        'aggregate_rating']].sort_values(by= 'aggregate_rating').head(select_quant_restaurant), use_container_width= True)

    st.divider()
    
with st.container():
    
    col1, col2 = st.columns(2)
    
    with col1:
        corpo = mk.aling(h = 'h4', text=f"Top {select_quant_restaurant} melhores tipos de culinárias" )
        st.markdown(corpo, unsafe_allow_html= True)
        
        cols = ['cuisines', 'aggregate_rating']
        aux = df1[cols].groupby('cuisines').mean('aggregate_rating').sort_values('aggregate_rating', ascending = False).reset_index().head(select_quant_restaurant)
        bar = px.bar(aux, x = 'cuisines', y ='aggregate_rating',
                labels= {
                    'aggregate_rating': 'Avaliação',
                    'cuisines': 'Culinária'
                })
        st.plotly_chart(bar, use_container_width= True)
        
    with col2:
        corpo = mk.aling(h = 'h4', text=f"Top {select_quant_restaurant} piores tipos de culinárias" )
        st.markdown(corpo, unsafe_allow_html= True)
        
        cols = ['cuisines', 'aggregate_rating']
        aux = df1[cols].groupby('cuisines').mean('aggregate_rating').sort_values('aggregate_rating', ascending = True).reset_index().head(select_quant_restaurant)
        aux = aux[aux['aggregate_rating']> 0]
        bar = px.bar(aux, x = 'cuisines', y ='aggregate_rating',
                labels= {
                    'aggregate_rating': 'Avaliação',
                    'cuisines': 'Culinária'
                })
        st.plotly_chart(bar, use_container_width= True)