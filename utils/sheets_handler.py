from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_IDS = {
    'planilha1': '16jzVhTNbJCE6_XyJIR-HGpI6nHChX_rz9ovKflGmBxM',
    'planilha2': '1KjJ3ygUQWOmOF_8y5w99vAsGtQhYVk1GVldXpHBNSvw'
}

def get_sheets_service():
    """
    Cria e retorna um serviço do Google Sheets
    """
    try:
        credentials = service_account.Credentials.from_service_account_file(
            'credentials.json', scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        raise Exception(f"Erro ao conectar com Google Sheets: {str(e)}")

def get_headers(spreadsheet_id, range_name='Página1'):
    """
    Obtém os cabeçalhos da planilha e suas posições
    """
    try:
        service = get_sheets_service()
        result = service.spreadsheets().values().get(
            spreadsheetId=spreadsheet_id,
            range=f'{range_name}!1:1'
        ).execute()
        
        headers = result.get('values', [[]])[0]
        header_positions = {header: index for index, header in enumerate(headers)}
        return header_positions
    except Exception as e:
        raise Exception(f"Erro ao obter cabeçalhos: {str(e)}")

def salvar_cliente_sheets(dados_cliente):
    """
    Salva os dados do cliente em ambas as planilhas
    """
    try:
        service = get_sheets_service()
        
        # Salvar na primeira planilha (controle de casos)
        header_positions1 = get_headers(SPREADSHEET_IDS['planilha1'])
        nova_linha1 = [''] * len(header_positions1)
        
        mapeamento1 = {
            'Cliente': dados_cliente['nome'],
            'Responsável_Comercial': dados_cliente['responsavel_comercial'],
            'Caso': dados_cliente['caso'],
            'Assunto Caso': dados_cliente['assunto_caso'],
            'Data_Entrada': dados_cliente['data']
        }
        
        for header, valor in mapeamento1.items():
            if header in header_positions1:
                nova_linha1[header_positions1[header]] = valor
                
        body1 = {'values': [nova_linha1]}
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_IDS['planilha1'],
            range='Página1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body1
        ).execute()
        
        # Salvar na segunda planilha (dados pessoais)
        header_positions2 = get_headers(SPREADSHEET_IDS['planilha2'])
        nova_linha2 = [''] * len(header_positions2)
        
        mapeamento2 = {
            'Nome': dados_cliente['nome'],
            'Email': dados_cliente['email'],
            'Celular': dados_cliente.get('celular', ''),
            'CPF': dados_cliente['cpf'],
            'RG': dados_cliente['rg'],
            'Data de Nascimento': dados_cliente.get('data_nascimento', ''),
            'Estado Civil': dados_cliente['estado_civil'],
            'Nacionalidade': dados_cliente['nacionalidade'],
            'Endereço': dados_cliente['rua'],
            'Bairro': dados_cliente['bairro'],
            'Cidade': dados_cliente['cidade'],
            'Estado': dados_cliente['estado'],
            'CEP': dados_cliente['cep']
        }
        
        for header, valor in mapeamento2.items():
            if header in header_positions2:
                nova_linha2[header_positions2[header]] = valor
                
        body2 = {'values': [nova_linha2]}
        service.spreadsheets().values().append(
            spreadsheetId=SPREADSHEET_IDS['planilha2'],
            range='Página1',
            valueInputOption='RAW',
            insertDataOption='INSERT_ROWS',
            body=body2
        ).execute()
        
        return True
        
    except Exception as e:
        raise Exception(f"Erro ao salvar no Google Sheets: {str(e)}") 