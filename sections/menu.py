import streamlit as st
import webbrowser

def menu_page():
    st.title("Menu Principal")
    
    # Seção de Links Rápidos
    st.header("Links Rápidos")
    
    # Estilo CSS para os botões
    button_style = """
    <style>
    .stButton > button {
        width: 100%;
        height: 50px;
        margin: 5px;
    }
    </style>
    """
    st.markdown(button_style, unsafe_allow_html=True)
    
    # Primeira linha de botões
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Clientes Smart Legal", use_container_width=True):
            webbrowser.open_new_tab("https://docs.google.com/spreadsheets/d/1KjJ3ygUQWOmOF_8y5w99vAsGtQhYVk1GVldXpHBNSvw/edit?gid=0#gid=0")
    with col2:
        if st.button("Processos Em Andamento", use_container_width=True):
            webbrowser.open_new_tab("https://docs.google.com/spreadsheets/d/16jzVhTNbJCE6_XyJIR-HGpI6nHChX_rz9ovKflGmBxM/edit?gid=0#gid=0")
    
    # Segunda linha de botões
    col3, col4 = st.columns(2)
    with col3:
        if st.button("Leads Ads", use_container_width=True):
            webbrowser.open_new_tab("https://docs.google.com/spreadsheets/d/14B_RE4JWqU6IxZyqdBJZHtjbhjy9a3C0KD1QkBziMFM/edit?gid=0#gid=0")
    with col4:
        if st.button("CRM RD Station", use_container_width=True):
            webbrowser.open_new_tab("https://crm.rdstation.com/app/deals/pipeline")
    
    # Terceira linha com um botão centralizado
    col5, col6 = st.columns(2)
    with col5:
        if st.button("Drive Gmail", use_container_width=True):
            webbrowser.open_new_tab("https://drive.google.com/drive/u/6/my-drive")
    
    # Seções existentes
    st.markdown("---")  # Separador
    st.header("Funcionalidades do Sistema")
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Onboarding")
        st.markdown("""
        - Cadastro de novos clientes
        - Geração automática de procuração
        - Upload e organização de documentos
        - Armazenamento no Google Drive
        """)
    
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