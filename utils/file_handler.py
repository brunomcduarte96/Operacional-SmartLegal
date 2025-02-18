import os
from utils.drive_handler import criar_pasta_drive, upload_arquivo

def criar_pasta_cliente(nome_cliente):
    """
    Cria uma pasta para o cliente no Google Drive
    """
    nome_pasta = nome_cliente.strip().replace(" ", "_")
    pasta_id = criar_pasta_drive(nome_pasta)
    
    # Criar pasta local temporária para processamento
    pasta_temp = os.path.join("temp", nome_pasta)
    if not os.path.exists(pasta_temp):
        os.makedirs(pasta_temp)
    
    return {'local': pasta_temp, 'drive_id': pasta_id}

def salvar_arquivos(pasta_info, comprovante_residencia, documento_identidade):
    """
    Salva os arquivos enviados na pasta do cliente
    """
    arquivos_salvos = []
    
    # Processar comprovante de residência
    if comprovante_residencia is not None:
        arquivo_info = {
            'name': comprovante_residencia.name,
            'content': comprovante_residencia,
            'type': 'comprovante_residencia',
            'drive_id': pasta_info['drive_id']
        }
        arquivos_salvos.append(arquivo_info)
    
    # Processar documento de identidade
    if documento_identidade is not None:
        arquivo_info = {
            'name': documento_identidade.name,
            'content': documento_identidade,
            'type': 'documento_identidade',
            'drive_id': pasta_info['drive_id']
        }
        arquivos_salvos.append(arquivo_info)
    
    return arquivos_salvos 