import streamlit as st

st.set_page_config(layout="wide") # Ajusta o layout para usar toda a largura

st.title("Minha Primeira Aplicação Streamlit")
st.write("Olá, mundo! Esta é uma aplicação Streamlit de teste.")
st.success("Se você vir esta mensagem, o Streamlit está funcionando!")

# Você pode adicionar seu código de análise de padrões aqui mais tarde
# from analise_padroes import AnalisePadroes # Se você mantiver em arquivos separados
# historico_exemplo = ['C', 'V', 'E', 'C', 'C', 'C', 'V', 'E', 'V', 'C']
# app_analise = AnalisePadroes(historico_exemplo)
# st.write("--- Padrões ---")
# st.write(app_analise.analisar_todos())
