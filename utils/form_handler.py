# Bibliotecas padrão
from datetime import datetime
import locale
import json
import io

# Bibliotecas de terceiros
import streamlit as st
import requests
from supabase import create_client, Client
from PIL import Image
import img2pdf

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

def converter_para_pdf(arquivo):
    """
    Converte diferentes tipos de arquivo para PDF usando img2pdf
    """
    if arquivo is None:
        return None
        
    # Pegar o tipo MIME do arquivo
    content_type = arquivo.type
    arquivo_bytes = arquivo.getvalue()
    
    # Se já for PDF, retorna os bytes direto
    if content_type == 'application/pdf':
        return arquivo_bytes
        
    # Se for imagem
    if content_type.startswith('image/'):
        try:
            # Converter imagem para PDF usando img2pdf
            image = Image.open(io.BytesIO(arquivo_bytes))
            # Converter para RGB se necessário
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Salvar imagem em bytes
            img_bytes = io.BytesIO()
            image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            
            # Converter para PDF
            pdf_bytes = img2pdf.convert(img_bytes.read())
            return pdf_bytes
            
        except Exception as e:
            st.error(f"Erro ao converter imagem para PDF: {str(e)}")
            return None
    
    return None

def upload_para_storage(supabase, arquivo, nome_arquivo, bucket="documentos-clientes"):
    """
    Faz upload do arquivo para o Supabase Storage e retorna a URL assinada
    """
    try:
        try:
            # Tentar remover arquivo existente (se houver)
            supabase.storage.from_(bucket).remove([nome_arquivo])
        except:
            pass  # Ignora se o arquivo não existir
            
        # Upload do arquivo
        response = supabase.storage.from_(bucket).upload(
            path=nome_arquivo,
            file=arquivo,
            file_options={"content-type": "application/pdf"}
        )
        
        # Gerar URL assinada (válida por 1 hora)
        file_url = supabase.storage.from_(bucket).create_signed_url(nome_arquivo, 3600)
        return file_url['signedURL']
        
    except Exception as e:
        st.error(f"Erro ao fazer upload do arquivo {nome_arquivo}: {str(e)}")
        return None

def enviar_para_webhook(webhook_url, webhook_data):
    """
    Função para enviar apenas dados JSON para o webhook
    """
    try:
        response = requests.post(
            webhook_url,
            json=webhook_data,
            verify=False,
            timeout=60
        )
        
        if response.status_code != 200:
            st.error(f"""
            Detalhes do erro do webhook:
            - Status: {response.status_code}
            - Resposta: {response.text[:500]}
            """)
            
        return response
        
    except Exception as e:
        st.error(f"Erro ao conectar com o webhook: {str(e)}")
        return None

def criar_formulario():
    """
    Cria o formulário de cadastro de cliente
    """
    # Adicionar toggle para ambiente de teste
    is_test = st.sidebar.checkbox("Ambiente de Teste", value=True)
    
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
            # Validar arquivos obrigatórios
            if not comprovante_residencia or not documento_identidade:
                st.error("Comprovante de Residência e Documento de Identidade são obrigatórios!")
                return None, False

            # Preparar dados para o Supabase
            dados_cliente_supabase = {
                'nome': capitalizar_nome(nome),
                'nacionalidade': nacionalidade,
                'estado_civil': estado_civil,
                'profissao': profissao,
                'rg': rg,
                'cpf': cpf,
                'rua': rua,
                'bairro': bairro,
                'complemento': complemento,
                'cep': cep,
                'cidade': cidade,
                'estado': estado,
                'email': email.lower(),
                'celular': celular,
                'data_nascimento': data_nascimento,
                'responsavel_comercial': responsavel_comercial
            }

            dados_processo_supabase = {
                'nome': capitalizar_nome(nome),
                'responsavel_comercial': responsavel_comercial,
                'caso': caso,
                'assunto_caso': assunto_caso,
                'status': 'Em Produção'
            }

            # Inicializar cliente Supabase
            supabase: Client = create_client(
                st.secrets["supabase_url"],
                st.secrets["supabase_key"]
            )

            try:
                # Inserir dados nas tabelas do Supabase
                response_cliente = supabase.table('Clientes_Ativos_SmartLegal').insert(dados_cliente_supabase).execute()
                response_processo = supabase.table('Processos_em_Andamento').insert(dados_processo_supabase).execute()

                # Upload dos documentos para o Storage
                arquivos_urls = {}
                todos_documentos_urls = []  # Array para todos os documentos
                
                # Processar comprovante de residência
                pdf_residencia = converter_para_pdf(comprovante_residencia)
                if pdf_residencia:
                    nome_arquivo = f"{cpf}/comprovante_residencia.pdf"
                    url = upload_para_storage(supabase, pdf_residencia, nome_arquivo)
                    if url:
                        arquivos_urls['comprovante_residencia_url'] = url
                        todos_documentos_urls.append({
                            'tipo': 'comprovante_residencia',
                            'nome': 'Comprovante de Residência',
                            'url': url
                        })
                    else:
                        st.error("Erro ao fazer upload do comprovante de residência")
                        return None, False

                # Processar documento de identidade
                pdf_identidade = converter_para_pdf(documento_identidade)
                if pdf_identidade:
                    nome_arquivo = f"{cpf}/documento_identidade.pdf"
                    url = upload_para_storage(supabase, pdf_identidade, nome_arquivo)
                    if url:
                        arquivos_urls['documento_identidade_url'] = url
                        todos_documentos_urls.append({
                            'tipo': 'documento_identidade',
                            'nome': 'Documento de Identidade',
                            'url': url
                        })
                    else:
                        st.error("Erro ao fazer upload do documento de identidade")
                        return None, False

                # Processar comprovantes adicionais
                comprovantes_extras_urls = []  # Array para comprovantes extras
                if comprovante_gastos:
                    for i, doc in enumerate(comprovante_gastos):
                        pdf_doc = converter_para_pdf(doc)
                        if pdf_doc:
                            nome_arquivo = f"{cpf}/comprovante_gastos_{i}.pdf"
                            url = upload_para_storage(supabase, pdf_doc, nome_arquivo)
                            if url:
                                arquivos_urls[f'comprovante_gastos_{i}_url'] = url
                                doc_info = {
                                    'tipo': 'comprovante_extra',
                                    'nome': f'Comprovante Extra {i+1}',
                                    'url': url
                                }
                                comprovantes_extras_urls.append(doc_info)
                                todos_documentos_urls.append(doc_info)

                # Preparar dados para o webhook
                webhook_data = {
                    **dados_cliente_supabase,
                    **dados_processo_supabase,
                    **arquivos_urls,
                    'quantidade_comprovantes_extras': len(comprovante_gastos) if comprovante_gastos else 0,
                    'comprovantes_extras_urls': comprovantes_extras_urls,  # Array só com extras
                    'todos_documentos_urls': todos_documentos_urls  # Array com todos os documentos
                }

                # Enviar dados para o webhook
                base_url = "https://n8n-n8n.hu1eyf.easypanel.host"
                webhook_path = "1a62b481-1010-4d3f-a20e-83efcd63d4dc"
                
                if is_test:
                    webhook_url = f"{base_url}/webhook-test/{webhook_path}"
                    st.info("Usando webhook de teste")
                else:
                    webhook_url = f"{base_url}/webhook/{webhook_path}"
                    
                response_webhook = enviar_para_webhook(webhook_url, webhook_data)
                
                if response_webhook and response_webhook.status_code == 200:
                    st.success("Cliente cadastrado com sucesso!")
                    if is_test:
                        st.json(response_webhook.json())
                else:
                    st.warning("""
                    Cliente cadastrado e documentos salvos, mas houve um problema ao notificar o sistema.
                    Por favor, informe ao suporte técnico.
                    """)
                    if is_test:
                        st.error(f"""
                        Detalhes do erro em teste:
                        Status: {response_webhook.status_code if response_webhook else 'N/A'}
                        URL: {webhook_url}
                        Resposta: {response_webhook.text if response_webhook else 'N/A'}
                        """)
                
                return dados_cliente_supabase, True
                    
            except Exception as e:
                # Remover qualquer menção ao Google Sheets do erro
                error_message = str(e)
                if "Google Sheets" in error_message or "JWT" in error_message:
                    error_message = "Erro interno ao processar o cadastro. Por favor, tente novamente."
                
                st.error(error_message)
                if is_test:
                    st.error(f"Erro original para debug: {str(e)}")
                return None, False

            return dados_cliente_supabase, True
            
    return None, False 