
import utils.transformation as ts
import plotly.express as px
import streamlit as st




paleta_cores = ['#3e4934','#dcdcdc ','#dd2026 ', '#80ada0' ,'#a10800' ,'#ddbb66' ,'#ddaa33']

#=============================================================================



#==========================================================================================================
def top_restaurants(df1, cores_paises):

    cols = ['restaurant_id', 'city', 'country_name']
    aux = df1.loc[:,cols].groupby(['country_name','city']).count().sort_values(by = 'restaurant_id', ascending= False).reset_index().head(10)
    fig = px.bar(aux, x = 'city', y = 'restaurant_id', 
            labels= {
                'city': 'Cidade',
                'restaurant_id':  'Qte de restaurantes'},
        color= 'country_name',
        color_discrete_map= cores_paises)
    return fig


def rest_star_higher(df1, cores_paises):
    cols = ['city','restaurant_id', 'country_name']
    aux = df1[df1['aggregate_rating'] >= 4]
    aux = aux.loc[:,cols].groupby(['country_name','city']).count().sort_values(by = 'restaurant_id', ascending= False).reset_index().head(10)
    fig = px.bar(aux, x = 'city', y = 'restaurant_id', 
                labels={
                    'city': 'Cidade',
                    'restaurant_id':'Quantidade de Restaurantes',
                    'country_name':'Pais'
                },
                color= 'country_name',
                color_discrete_map= cores_paises)
    return fig

def rest_star_lower(df1, cores_paises):
    cols = ['city','restaurant_id', 'country_name']
    aux = df1[df1['aggregate_rating'] <= 2.5]
    aux = aux.loc[:,cols].groupby(['country_name','city']).count().sort_values(by = 'restaurant_id', ascending= False).reset_index().head(15)
    aux.columns = ['country_name','city', 'num_restaurantes']

    fig = px.bar(aux, x = 'city', y = 'num_restaurantes', 
                labels={
                    'city': 'Cidade',
                    'num_restaurantes':'Quantidade de Restaurantes',
                    'country_name':'Pais'
                },
                color= 'country_name',
                color_discrete_map= cores_paises)
    return fig

def top_cuisines(df1, cores_paises):
    cols = ['city', 'cuisines', 'country_name']
    aux = df1[cols].groupby(['city', 'country_name']).nunique().sort_values(by='cuisines', ascending=False).reset_index().head(10)
    fig = px.bar(aux, x='city', y='cuisines',
                    labels= {'cuisines': 'Culinária', 'country_name': 'Pais', 'city': 'Cidade'},
                    color= 'country_name',
                    color_discrete_map= cores_paises)
    return fig

