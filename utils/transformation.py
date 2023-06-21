import inflection
import streamlit as st


# Taxas de câmbio em relação ao dólar adiquidas no dia 21/06/2023
taxas = {
    'Botswana Pula(P)': 0.075,  
    'Brazilian Real(R$)': 0.21,  
    'Dollar($)': 1.0, 
    'Emirati Diram(AED)': 0.27,  
    'Indian Rupees(Rs.)': 0.012,  
    'Indonesian Rupiah(IDR)': 0.000067,  
    'NewZealand($)': 0.62,  
    'Pounds(£)': 1.27,  
    'Qatari Rial(QR)': 0.27,  
    'Rand(R)': 0.054,  
    'Sri Lankan Rupee(LKR)': 0.0032,  
    'Turkish Lira(TL)': 0.42  
}

# Função para converter a moeda para dólar
def converter_para_dolar(moeda, valor):
    if moeda in taxas:
        taxa = taxas[moeda]
        valor_em_dolar = valor * taxa
        return valor_em_dolar
    else:
        return None


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
    
    #9. Convertendo valores de average_cost_for_two para Dollar
    df1['average_cost_for_two_dollar'] = df1[['average_cost_for_two', 'currency']].apply(lambda x: converter_para_dolar(x['currency'], x['average_cost_for_two'] ), axis = 1)    
    return df1