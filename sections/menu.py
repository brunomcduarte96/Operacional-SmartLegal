import streamlit as st

def menu_page():
    st.title("Menu Principal")
    
    # Seção Principal
    st.header("Funcionalidades Principais")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Onboarding")
        st.markdown("""
        - Cadastro de novos clientes
        - Geração automática de procuração
        - Upload e organização de documentos
        - Armazenamento no Google Drive
        """)
        
        st.subheader("Consulta de Clientes")
        st.markdown("""
        - Visualização de todos os clientes
        - Busca por CPF
        - Acesso aos dados cadastrais
        - Histórico de documentos
        """)
    
    # Seção Aéreo
    with col2:
        st.subheader("Módulo Aéreo")
        st.markdown("""
        #### Atraso / Cancelamento de Voo
        - Geração de petições iniciais
        - Cálculo de indenizações
        - Jurisprudência específica
        
        #### Extravio de Bagagem
        - Petições automatizadas
        - Cálculo de danos materiais
        - Precedentes judiciais
        
        #### Downgrade
        - Petições personalizadas
        - Cálculo de reembolsos
        - Normas ANAC
        
        #### Overbooking
        - Modelos específicos
        - Indenizações padronizadas
        - Base de jurisprudência
        """) 