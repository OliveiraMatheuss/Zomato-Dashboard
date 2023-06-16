import inflection
import streamlit as st



def metric_cuisine(df1, culinaria):
        cuisine_aux = cuisines_ratting(df = df1, cuisine= culinaria, ascending= False).head(1)
        st.metric(label = f"{culinaria}: {cuisine_aux['restaurant_name'].values[0]}\n",
                    value= f"{cuisine_aux['aggregate_rating'].values[0]}/5.0",
                    help = f"""
                    País: {cuisine_aux['country_name'].values[0]}\n
                    Cidade: {cuisine_aux['city'].values[0]}\n
                    Média Prato para dois: {cuisine_aux['average_cost_for_two'].values[0]}\n
                    """)
        return 

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
    #df1 = df1[(df1['average_cost_for_two'] != 0) & (df1['aggregate_rating'] !=0)]
    
    return df1