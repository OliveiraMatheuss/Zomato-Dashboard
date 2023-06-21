#==========================================================================================================#
#===================================== IMPORTAÇÕES ========================================================#
#==========================================================================================================#

import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
from millify import millify as mil
from utils import transformation as ts

st.set_page_config(page_title= 'Home',
                    page_icon="chart_with_upwards_trend",
                    layout= 'wide')

#==========================================================================================================#
#================================= FUNÇÕES ================================================================#
#==========================================================================================================#

def mapMaker(df):
    
    "Cria um mapa de acordo com o df passado "
    folium.Figure(width=1920, height=768)
    aux = df.copy()
    map = folium.Map(location= [0,0], zoom_start= 2)
    make_cluster = MarkerCluster().add_to(map)

    for intex, df in aux.iterrows():
        
        restaurante = df['restaurant_name']
        cuisises = df['cuisines']
        rating = df['aggregate_rating']
        
        html = '<p><strong> {} </strong></p>'
        html += '<p>{}</p>'
        html += '<p>{}</p>'
        pp = folium.Html(html.format(restaurante,cuisises,rating),script= True)
        folium.Marker(location= [df['latitude'],df['longitude']],
                        icon= folium.Icon(color = df['rating_color_name']),
                        popup= folium.Popup(pp, max_width=500)
                        ).add_to(make_cluster)
    folium_static(map, width=1024, height=600)
        

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
                                            options = df1.country_name.unique(),
                                            default=  df1.country_name.unique())

# filtros

select_country = df1[df1['country_name'].isin(select_country_mult)]

#==============================================================================================================#
#====================================    LAYOUT      ==========================================================#
#==============================================================================================================#

original_title = '<h1 style="font-family:Courier; color:White; font-size: 40px;">Zomato</h1>'

st.markdown(original_title, unsafe_allow_html= True)
st.markdown('## O Melhor lugar para encontrar seu mais novo restaurante favorito!')

with st.container():
    st.markdown("### Temos as seguintes marcas dentro da nossa plataforma:")
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        num_restaurantes = df1['restaurant_id'].nunique()
        col1.metric(label= 'Restaurantes Cadastrados', value = mil(num_restaurantes, precision = 2))
    
    with col2:
        num_pais = df1['country_code'].nunique()
        col2.metric(label= 'Paises Cadastrados', value = num_pais )
        
    with col3: 
        num_cidades = df1['city'].nunique()
        col3.metric(label= 'Cidades Cadastradas', value= num_cidades)
    
    with col4:
        total_votes = df1['votes'].sum()
        col4.metric(label= 'Avaliações feitas na plataforma', value = mil(total_votes, precision= 2))
    with col5:
        total_cuisines = df1['cuisines'].nunique()
        col5.metric(label = 'Tipos de Cuniárias Oferecidas,', value=  total_cuisines )
        
        
with st.container():
    mapMaker(select_country)