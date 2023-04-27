#==========================================================================================================#
#===================================== IMPORTAÇÕES ========================================================#
#==========================================================================================================#

import pandas as pd
import plotly.express as px
import folium
import streamlit as st
from streamlit_folium import folium_static
import inflection
from folium.plugins import MarkerCluster
from millify import millify as mil

st.set_page_config(page_title= 'Home',
                    layout= 'wide')


#==========================================================================================================#
#================================= FUNÇÕES ================================================================#
#==========================================================================================================#

def rename_columns(dataframe):
    
    """
        renomea as colunas do dataset

    """
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df



def create_price_tye(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"



def cuisines_ratting(df, cuisine, ascending = True):
    cols = ['restaurant_name', 'country_name', 'aggregate_rating']
    df = df[df.cuisines.isin([cuisine])]
    df = df[cols]

    return df.sort_values('aggregate_rating', ascending= ascending)

def limpeza(df1):
    
    COLORS = {
                "3F7E00": "darkgreen",
                "5BA829": "green",
                "9ACD32": "lightgreen",
                "CDD614": "orange",
                "FFBA00": "red",
                "CBCBC8": "darkred",
                "FF7800": "darkred",
                }
    
    COUNTRIES = {
                    1: "India",
                    14: "Australia",
                    30: "Brazil",
                    37: "Canada",
                    94: "Indonesia",
                    148: "New Zeland",
                    162: "Philippines",
                    166: "Qatar",
                    184: "Singapure",
                    189: "South Africa",
                    191: "Sri Lanka",
                    208: "Turkey",
                    214: "United Arab Emirates",
                    215: "England",
                    216: "United States of America",
                    }
    
    df1 = df1.copy()

    # 0. Mudar nome das colunas
    df1 = rename_columns(df1)
    # 1. Transformar o tipo int para object na coluna "Restauran ID"
    df1['restaurant_id'] = df1.loc[:,'restaurant_id'].astype(str)

    #2 Remover valores ausentes nan
    df1.dropna(inplace= True)

    #3. categorizar por um tipo de culinaria
    df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

    #4. Remover valores duplicados
    df1.drop_duplicates(inplace= True)

    #5. Alterando variavel categorica price_range
    df1['price_range'] = df1['price_range'].apply(lambda x: create_price_tye(x))

    #6. Criando a coluna country_name
    df1['country_name'] = df1['country_code'].map(COUNTRIES)

    #7. Criando a coluna color_name
    df1['rating_color_name'] = df1['rating_color'].map(COLORS)

    #8. Removendo pratos que são iguais a zero
    df1 = df1[(df1['average_cost_for_two'] != 0) & (df1['aggregate_rating'] !=0)]
    
    return df1


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
df1 = limpeza(df)



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



st.title('FOME ZERO!')
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