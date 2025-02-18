import streamlit as st
from utils.database import listar_clientes, buscar_cliente_por_cpf

def clientes_page():
    st.title("Consulta de Clientes")
    
    # Criar tabs para diferentes tipos de consulta
    tab1, tab2 = st.tabs(["Lista de Clientes", "Busca por CPF"])
    
    # Tab de Lista de Clientes
    with tab1:
        try:
            clientes = listar_clientes()
            
            if not clientes:
                st.info("Nenhum cliente cadastrado.")
                return
            
            # Criar uma tabela com os clientes
            st.write("### Clientes Cadastrados")
            
            # Criar colunas para a tabela
            cols = st.columns([3, 2, 2, 2])
            cols[0].write("**Nome**")
            cols[1].write("**CPF**")
            cols[2].write("**Cidade**")
            cols[3].write("**Detalhes**")
            
            # Listar os clientes
            for cliente in clientes:
                cols = st.columns([3, 2, 2, 2])
                cols[0].write(cliente['nome'])
                cols[1].write(cliente['cpf'])
                cols[2].write(cliente['cidade'])
                
                # Botão para ver detalhes
                if cols[3].button("Ver", key=f"btn_{cliente['cpf']}"):
                    mostrar_detalhes_cliente(cliente)
        
        except Exception as e:
            st.error(f"Erro ao carregar lista de clientes: {str(e)}")
    
    # Tab de Busca por CPF
    with tab2:
        cpf_busca = st.text_input("Digite o CPF do cliente:")
        if st.button("Buscar"):
            if cpf_busca:
                try:
                    cliente = buscar_cliente_por_cpf(cpf_busca)
                    if cliente:
                        mostrar_detalhes_cliente(cliente)
                    else:
                        st.warning("Cliente não encontrado.")
                except Exception as e:
                    st.error(f"Erro ao buscar cliente: {str(e)}")
            else:
                st.warning("Por favor, digite um CPF para buscar.")

def mostrar_detalhes_cliente(cliente):
    """
    Mostra os detalhes do cliente em um formato organizado
    """
    st.write("---")
    st.write("### Detalhes do Cliente")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Dados Pessoais**")
        st.write(f"Nome: {cliente['nome']}")
        st.write(f"Nacionalidade: {cliente['nacionalidade']}")
        st.write(f"Estado Civil: {cliente['estado_civil']}")
        st.write(f"Profissão: {cliente['profissao']}")
        st.write(f"RG: {cliente['rg']}")
        st.write(f"CPF: {cliente['cpf']}")
    
    with col2:
        st.write("**Endereço**")
        st.write(f"Rua: {cliente['rua']}")
        st.write(f"Bairro: {cliente['bairro']}")
        st.write(f"Complemento: {cliente['complemento']}")
        st.write(f"CEP: {cliente['cep']}")
        st.write(f"Cidade: {cliente['cidade']}")
        st.write(f"Estado: {cliente['estado']}") 