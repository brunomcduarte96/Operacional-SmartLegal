import streamlit as st
import os
from datetime import datetime
from utils.form_handler import criar_formulario
from utils.file_handler import criar_pasta_cliente, salvar_arquivos
from utils.pdf_generator import converter_para_pdf, combinar_comprovantes_gastos, combinar_todos_documentos
from utils.document_handler import gerar_procuracao
import shutil

def main():
    st.title("Sistema de Cadastro de Clientes")
    
    # Criar formulário e capturar dados
    dados_cliente, submitted = criar_formulario()
    
    if submitted:
        if dados_cliente['nome']:
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            try:
                # Criar pasta do cliente (local e Drive)
                status_text.text("Criando pasta do cliente...")
                pasta_info = criar_pasta_cliente(dados_cliente['nome'])
                progress_bar.progress(10)
                
                # Processar documentos individuais
                status_text.text("Processando documentos individuais...")
                arquivos_pdf = salvar_arquivos(
                    pasta_info,
                    dados_cliente['comprovante_residencia'],
                    dados_cliente['documento_identidade']
                )
                pdfs_gerados = converter_para_pdf(
                    pasta_info,
                    arquivos_pdf,
                    dados_cliente['nome']
                )
                progress_bar.progress(40)
                
                # Processar comprovantes de gastos
                status_text.text("Processando comprovantes de gastos...")
                if dados_cliente['comprovante_gastos']:
                    comprovantes_gastos_pdf = combinar_comprovantes_gastos(
                        pasta_info,
                        dados_cliente['comprovante_gastos'],
                        dados_cliente['nome']
                    )
                progress_bar.progress(70)
                
                # Combinar todos os documentos
                status_text.text("Combinando todos os documentos...")
                combinar_todos_documentos(pasta_info, dados_cliente['nome'])
                progress_bar.progress(85)
                
                # Gerar e salvar procuração
                status_text.text("Gerando procuração...")
                gerar_procuracao(pasta_info, dados_cliente)
                progress_bar.progress(100)
                
                # Limpar arquivos temporários ao final
                if os.path.exists(pasta_info['local']):
                    shutil.rmtree(pasta_info['local'])
                
                status_text.empty()
                st.success("Cadastro realizado com sucesso! Documentos salvos no Google Drive.")
                
            except Exception as e:
                progress_bar.empty()
                status_text.empty()
                st.error(f"Erro ao processar o cadastro: {str(e)}")
                
        else:
            st.error("Por favor, preencha pelo menos o nome do cliente.")

if __name__ == "__main__":
    main() 