import streamlit as st
from datetime import datetime
import locale

def capitalizar_nome(texto):
    """
    Capitaliza a primeira letra de cada palavra no texto
    """
    if not texto:
        return texto
    return ' '.join(word.capitalize() for word in texto.split())

def capitalizar_primeira_letra(texto):
    """
    Capitaliza apenas a primeira letra do texto
    """
    if not texto:
        return texto
    return texto[0].upper() + texto[1:].lower() if len(texto) > 1 else texto.upper()

def criar_formulario():
    """
    Cria o formulário de cadastro do cliente e retorna os dados preenchidos
    """
    dados_cliente = {}
    submitted = False
    
    with st.form("formulario_cliente"):
        # Dados pessoais
        nome_input = st.text_input("Nome completo")
        nacionalidade_input = st.text_input("Nacionalidade")
        estado_civil = st.selectbox(
            "Estado Civil",
            ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)"]
        )
        profissao_input = st.text_input("Profissão")
        
        # Documentos
        rg = st.text_input("RG")
        cpf = st.text_input("CPF")
        
        # Endereço
        rua_input = st.text_input("Rua")
        bairro_input = st.text_input("Bairro")
        complemento_input = st.text_input("Complemento")
        cep = st.text_input("CEP")
        cidade_input = st.text_input("Cidade")
        estado_input = st.text_input("Estado")
        
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
        
        if submitted:
            # Capitalizar os dados após o envio do formulário
            dados_cliente['nome'] = capitalizar_nome(nome_input)
            dados_cliente['nacionalidade'] = capitalizar_primeira_letra(nacionalidade_input)
            dados_cliente['estado_civil'] = estado_civil  # Já está capitalizado
            dados_cliente['profissao'] = capitalizar_primeira_letra(profissao_input)
            dados_cliente['rg'] = rg  # Manter original para documentos
            dados_cliente['cpf'] = cpf  # Manter original para documentos
            dados_cliente['rua'] = capitalizar_nome(rua_input)
            dados_cliente['bairro'] = capitalizar_nome(bairro_input)
            dados_cliente['complemento'] = capitalizar_primeira_letra(complemento_input)
            dados_cliente['cep'] = cep  # Manter original para CEP
            dados_cliente['cidade'] = capitalizar_nome(cidade_input)
            dados_cliente['estado'] = capitalizar_nome(estado_input)
    
    return dados_cliente, submitted 