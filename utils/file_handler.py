import os
import shutil
from pathlib import Path

def criar_pasta_cliente(nome_cliente):
    """
    Cria uma pasta para o cliente dentro do diretório 'clientes'
    """
    nome_pasta = nome_cliente.strip().replace(" ", "_")
    pasta_cliente = os.path.join("clientes", nome_pasta)
    
    if not os.path.exists(pasta_cliente):
        os.makedirs(pasta_cliente)
    
    return pasta_cliente

def salvar_arquivos(pasta_cliente, comprovante_residencia, documento_identidade):
    """
    Salva os arquivos enviados na pasta do cliente
    """
    arquivos_salvos = []
    
    # Processar comprovante de residência
    if comprovante_residencia is not None:
        arquivo_info = {
            'name': comprovante_residencia.name,
            'content': comprovante_residencia,
            'type': 'comprovante_residencia'
        }
        arquivos_salvos.append(arquivo_info)
    
    # Processar documento de identidade
    if documento_identidade is not None:
        arquivo_info = {
            'name': documento_identidade.name,
            'content': documento_identidade,
            'type': 'documento_identidade'
        }
        arquivos_salvos.append(arquivo_info)
    
    return arquivos_salvos 