import streamlit as st
from datetime import datetime
import locale

def capitalizar_nome(nome):
    """
    Capitaliza a primeira letra de cada palavra no nome
    """
    if not nome:
        return nome
    return ' '.join(word.capitalize() for word in nome.split())

def criar_formulario():
    """
    Cria o formulário de cadastro do cliente e retorna os dados preenchidos
    """
    dados_cliente = {}
    submitted = False
    
    with st.form("formulario_cliente"):
        # Dados pessoais
        nome_input = st.text_input("Nome completo")
        dados_cliente['nome'] = capitalizar_nome(nome_input)
        dados_cliente['nacionalidade'] = st.text_input("Nacionalidade")
        dados_cliente['estado_civil'] = st.selectbox(
            "Estado Civil",
            ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]
        )
        dados_cliente['profissao'] = st.text_input("Profissão")
        
        # Documentos
        dados_cliente['rg'] = st.text_input("RG")
        dados_cliente['cpf'] = st.text_input("CPF")
        
        # Endereço
        dados_cliente['rua'] = st.text_input("Rua")
        dados_cliente['bairro'] = st.text_input("Bairro")
        dados_cliente['complemento'] = st.text_input("Complemento")
        dados_cliente['cep'] = st.text_input("CEP")
        dados_cliente['cidade'] = st.text_input("Cidade")
        dados_cliente['estado'] = st.text_input("Estado")
        
        # Upload de arquivos
        dados_cliente['comprovante_residencia'] = st.file_uploader(
            "Comprovante de Residência",
            type=['pdf', 'png', 'jpg', 'jpeg']
        )
        dados_cliente['documento_identidade'] = st.file_uploader(
            "Documento de Identidade",
            type=['pdf', 'png', 'jpg', 'jpeg']
        )
        dados_cliente['comprovante_gastos'] = st.file_uploader(
            "Comprovante de Gastos",
            type=['pdf', 'png', 'jpg', 'jpeg'],
            accept_multiple_files=True
        )
        
        # Configurar locale para português do Brasil
        try:
            locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
            except locale.Error:
                st.warning("Não foi possível configurar o idioma para português. As datas serão exibidas no formato padrão.")
        
        # Data atual por extenso em português
        data_atual = datetime.now()
        dados_cliente['data'] = data_atual.strftime("%d de %B de %Y")
        
        submitted = st.form_submit_button("Enviar Formulário")
    
    return dados_cliente, submitted 