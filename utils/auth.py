import streamlit as st
from supabase import create_client

def init_auth():
    """Inicializa a autenticação"""
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    if 'user' not in st.session_state:
        st.session_state.user = None

def login_page():
    """Página de login"""
    st.title("Login")
    
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")
        submitted = st.form_submit_button("Entrar")
        
        if submitted:
            try:
                # Inicializar cliente Supabase
                supabase = create_client(
                    st.secrets["supabase_url"],
                    st.secrets["supabase_key"]
                )
                
                # Tentar fazer login
                response = supabase.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })
                
                # Login bem sucedido
                st.session_state.authenticated = True
                st.session_state.user = response.user
                st.success("Login realizado com sucesso!")
                st.rerun()
                
            except Exception as e:
                st.error("Email ou senha inválidos")

def logout():
    """Fazer logout"""
    st.session_state.authenticated = False
    st.session_state.user = None
    st.rerun() 