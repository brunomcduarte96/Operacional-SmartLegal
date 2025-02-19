import streamlit as st
from utils.form_handler import criar_formulario

def onboarding_page():
    st.title("Onboarding de Clientes")
    
    # Criar formulário e capturar dados
    dados_cliente, submitted = criar_formulario()
    
    if submitted and dados_cliente:
        st.success("Cliente cadastrado com sucesso!") 