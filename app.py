import streamlit as st
from sections.onboarding import onboarding_page
from sections.iniciais_aereo import iniciais_aereo_page
from sections.extravio_bagagem import extravio_bagagem_page
from sections.downgrade import downgrade_page
from sections.overbooking import overbooking_page
from sections.menu import menu_page
from utils.auth import init_auth, login_page, logout
import os

def main():
    # Configuração da página
    st.set_page_config(
        page_title="Sistema Jurídico",
        page_icon="⚖️",
        layout="wide"
    )
    
    # Inicializar autenticação
    init_auth()
    
    # Verificar se usuário está autenticado
    if not st.session_state.authenticated:
        login_page()
        return
        
    # Botão de logout no sidebar
    if st.sidebar.button("Logout"):
        logout()
        return
    
    # Mostrar usuário logado
    st.sidebar.write(f"Usuário: {st.session_state.user.email}")
    
    # Inicializar a página padrão se não houver nenhuma selecionada
    if 'pagina' not in st.session_state:
        st.session_state.pagina = "Menu"  # Alterado para começar no Menu
    
    # Menu lateral - Seção Principal
    st.sidebar.title("Menu Principal")
    if st.sidebar.button("Menu", use_container_width=True):
        st.session_state.pagina = "Menu"
    if st.sidebar.button("Onboarding", use_container_width=True):
        st.session_state.pagina = "Onboarding"
    
    # Separador visual
    st.sidebar.markdown("---")
    
    # Menu lateral - Seção Aéreo
    st.sidebar.title("Aéreo")
    if st.sidebar.button("Atraso / Cancelamento de Voo", use_container_width=True):
        st.session_state.pagina = "Gerar Iniciais Aéreo"
    if st.sidebar.button("Extravio de Bagagem", use_container_width=True):
        st.session_state.pagina = "Extravio Bagagem"
    if st.sidebar.button("Downgrade", use_container_width=True):
        st.session_state.pagina = "Downgrade"
    if st.sidebar.button("Overbooking", use_container_width=True):
        st.session_state.pagina = "Overbooking"
    
    # Debug: Mostrar página atual
    st.sidebar.markdown("---")
    st.sidebar.write(f"Página atual: {st.session_state.pagina}")
    
    # Verificar estrutura de arquivos
    st.sidebar.write("Debug - Arquivos:")
    st.sidebar.write(f"sections existe: {os.path.exists('sections')}")
    st.sidebar.write(f"clientes.py existe: {os.path.exists('sections/clientes.py')}")
    
    # Renderizar página selecionada
    try:
        if st.session_state.pagina == "Menu":
            menu_page()
        elif st.session_state.pagina == "Onboarding":
            onboarding_page()
        elif st.session_state.pagina == "Gerar Iniciais Aéreo":
            iniciais_aereo_page()
        elif st.session_state.pagina == "Extravio Bagagem":
            extravio_bagagem_page()
        elif st.session_state.pagina == "Downgrade":
            downgrade_page()
        elif st.session_state.pagina == "Overbooking":
            overbooking_page()
    except Exception as e:
        st.error(f"Erro ao carregar página: {str(e)}")

if __name__ == "__main__":
    main() 