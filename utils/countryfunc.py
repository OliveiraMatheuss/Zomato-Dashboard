import plotly.express as px


paleta_cores = ['#3e4934','#dcdcdc ','#dd2026 ', '#80ada0' ,'#a10800' ,'#ddbb66' ,'#ddaa33']


def restaurants(df1,cores_paises):
    cols = ['country_name', 'restaurant_id']
    aux = df1.loc[:,cols].groupby('country_name').count().sort_values( by= 'restaurant_id',ascending=False).head(10).reset_index().head()
    aux = aux.sort_values( by= 'restaurant_id',ascending=True)
    fig = px.bar(aux, y = 'country_name', x = 'restaurant_id',
                text_auto= '.2s',
                orientation= 'h',
                labels= {
                    'country_name': 'Pais',
                    'restaurant_id': 'Qtd de Restaurantes'
                },
                color= 'country_name',
                color_discrete_map= cores_paises)

    return fig

def city(df1,cores_paises):
    cols = ['country_name','city','restaurant_id']
    aux = df1.loc[:,cols].groupby(['country_name', 'city']).count().reset_index()
    aux = aux.loc[:,['country_name', 'city']].groupby('country_name').count().sort_values(by = 'city',ascending=False).reset_index().head()
    aux = aux.sort_values( by= 'city',ascending=True)
    fig = px.bar(aux, y = 'country_name', x = 'city',
                        text_auto= '.2s',
                        orientation= 'h',
                        labels={
                                'country_name' : 'Pais',
                                'city': 'Qtd de Cidades'},
                        color= 'country_name',
                        color_discrete_map= cores_paises)

    return fig

def votes(df1,cores_paises):
    cols = ['country_name','votes']
    aux = df1.loc[:,cols].groupby('country_name').mean().sort_values(by = 'votes', ascending= False).reset_index().head(10)
    fig = px.bar(aux, x = 'country_name', y = 'votes',
                        text_auto= '.2s',
                        labels= {
                                'country_name': 'Pais',
                                'votes': 'Quantidade de Avaliações'},
                        color= 'country_name',
                color_discrete_map= cores_paises)

    return fig

def price(df1,cores_paises):
    cols = ['country_name', 'average_cost_for_two_dollar']
    aux = df1[cols].groupby('country_name').mean('average_cost_for_two_dollar')
    aux = aux.reset_index()
    aux = aux.sort_values(by = 'average_cost_for_two_dollar', ascending= False).head(10)
    fig = px.bar(aux, x = 'country_name', y = 'average_cost_for_two_dollar', 
                        text_auto= '.2s',
                        labels ={
                                'country_name': 'Pais',
                                'average_cost_for_two_dollar': 'Preço Médio'},
                        color= 'country_name',
                        color_discrete_map= cores_paises)

    return fig

def aggregate_rating_higher(df1,cores_paises):  
    
    cols = ['country_name', 'aggregate_rating']
    aux = df1.loc[:,cols].groupby('country_name').mean('aggregate_rating')
    aux = aux.reset_index()
    aux = aux.sort_values(by = 'aggregate_rating',ascending = False).head(10)
    fig = px.bar(aux, x = 'country_name', y = 'aggregate_rating',
                text_auto= '.2s',
                labels= {
                        'country_name': 'Pais',
                        'aggregate_rating': 'Avaliação'},
                color= 'country_name',
                color_discrete_map= cores_paises)

    return fig


def aggregate_rating_lower(df1,cores_paises):
    cols = ['country_name', 'aggregate_rating']
    aux = df1.loc[:,cols].groupby('country_name').mean('aggregate_rating')
    aux = aux.reset_index()
    aux = aux.sort_values(by = 'aggregate_rating').head(10)
    fig = px.bar(aux, x = 'country_name', y = 'aggregate_rating',
                    text_auto= '.2s',
                    labels= {
                            'country_name': 'Pais',
                            'aggregate_rating': 'Avaliação'},
                    color= 'country_name',
                color_discrete_map= cores_paises)

    return fig