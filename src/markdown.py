import streamlit as st 


st.markdown("<h3 style='text-align: center'> Quantidade de Restaurantes por Pais </h3>", unsafe_allow_html=True)
def aling(h = 'h1',text = 'title'):
    corpo = "<" + h
    corpo += ' style=' + 'text-align: center' + '> '
    corpo += text
    return  st.markdown(corpo, unsafe_allow_html=True)