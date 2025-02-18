from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import os

SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'credentials.json'
PASTA_PRINCIPAL_ID = '19_l1fTXv2_KR7BeXK9b64YsJ4ov2GX4M'  # ID da pasta "Clientes" do Drive

def get_drive_service():
    """
    Cria e retorna um serviço do Google Drive
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        return build('drive', 'v3', credentials=credentials)
    except Exception as e:
        raise Exception(f"Erro ao conectar com Google Drive: {str(e)}")

def criar_pasta_drive(nome_cliente):
    """
    Cria uma pasta para o cliente dentro da pasta Clientes no Drive
    """
    try:
        service = get_drive_service()
        
        # Criar pasta do cliente dentro da pasta Clientes
        file_metadata = {
            'name': nome_cliente,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [PASTA_PRINCIPAL_ID]
        }
        
        pasta = service.files().create(body=file_metadata, fields='id').execute()
        return pasta.get('id')
        
    except Exception as e:
        raise Exception(f"Erro ao criar pasta no Drive: {str(e)}")

def upload_arquivo(pasta_id, nome_arquivo, conteudo, mime_type='application/pdf'):
    """
    Faz upload de um arquivo para o Google Drive
    """
    try:
        service = get_drive_service()
        
        file_metadata = {
            'name': nome_arquivo,
            'parents': [pasta_id]
        }
        
        # Criar objeto MediaIoBaseUpload para o upload
        if isinstance(conteudo, bytes):
            media = MediaIoBaseUpload(
                io.BytesIO(conteudo),
                mimetype=mime_type,
                resumable=True
            )
        else:
            media = MediaIoBaseUpload(
                io.BytesIO(conteudo.read()),
                mimetype=mime_type,
                resumable=True
            )
        
        # Fazer o upload
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        return file.get('id')
        
    except Exception as e:
        raise Exception(f"Erro ao fazer upload do arquivo: {str(e)}") 