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
    Cria o formulário de cadastro de cliente
    """
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
    st.write(f"Data atual: {data_atual.strftime('%d de %B de %Y')}")
    
    with st.form("cadastro_cliente"):
        st.write("### Dados do Cliente")
        
        # Dados pessoais
        nome = st.text_input("Nome completo")
        nacionalidade = st.text_input("Nacionalidade", value="Brasileiro(a)")
        estado_civil = st.selectbox(
            "Estado Civil",
            ["Solteiro(a)", "Casado(a)", "Divorciado(a)", "Viúvo(a)", "União Estável"]
        )
        profissao = st.text_input("Profissão")
        email = st.text_input("E-mail")
        celular = st.text_input("Celular")
        data_nascimento = st.text_input("Data de Nascimento")
        
        # Documentos
        col1, col2 = st.columns(2)
        with col1:
            rg = st.text_input("RG")
        with col2:
            cpf = st.text_input("CPF")
            
        # Informações do Caso
        st.write("### Informações do Caso")
        col3, col4, col5 = st.columns(3)
        with col3:
            caso = st.selectbox(
                "Caso",
                ["Aéreo", "Trânsito", "Outros"]
            )
        with col4:
            assunto_caso = st.selectbox(
                "Assunto do Caso",
                [
                    "Atraso de Voo",
                    "Cancelamento de Voo",
                    "Overbooking",
                    "Downgrade",
                    "Extravio de Bagagem",
                    "Danos de Bagagem",
                    "Multas",
                    "Lei Seca",
                    "Outros"
                ]
            )
        with col5:
            responsavel_comercial = st.selectbox(
                "Responsável Comercial",
                [
                    "Bruno",
                    "Poppe",
                    "Motta",
                    "Caval",
                    "Fred",
                    "Mari",
                    "Outro"
                ]
            )
            
        # Endereço
        st.write("### Endereço")
        rua = st.text_input("Rua")
        complemento = st.text_input("Complemento")
        bairro = st.text_input("Bairro")
        cidade = st.text_input("Cidade")
        estado = st.text_input("Estado")
        cep = st.text_input("CEP")
        
        # Upload de documentos
        st.write("### Documentos")
        comprovante_residencia = st.file_uploader("Comprovante de Residência", type=['pdf', 'png', 'jpg', 'jpeg'])
        documento_identidade = st.file_uploader("Documento de Identidade", type=['pdf', 'png', 'jpg', 'jpeg'])
        comprovante_gastos = st.file_uploader("Outros Comprovantes (opcional)", type=['pdf', 'png', 'jpg', 'jpeg'], accept_multiple_files=True)
        
        submitted = st.form_submit_button("Cadastrar")
        
        if submitted:
            dados_cliente = {
                'nome': nome,
                'nacionalidade': nacionalidade,
                'estado_civil': estado_civil,
                'profissao': profissao,
                'email': email,
                'celular': celular,
                'data_nascimento': data_nascimento,
                'rg': rg,
                'cpf': cpf,
                'caso': caso,
                'assunto_caso': assunto_caso,
                'responsavel_comercial': responsavel_comercial,
                'rua': rua,
                'complemento': complemento,
                'bairro': bairro,
                'cidade': cidade,
                'estado': estado,
                'cep': cep,
                'comprovante_residencia': comprovante_residencia,
                'documento_identidade': documento_identidade,
                'comprovante_gastos': comprovante_gastos,
                'data': datetime.now().strftime("%d/%m/%Y")
            }
            return dados_cliente, submitted
            
    return None, False 