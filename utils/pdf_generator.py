from PIL import Image
import img2pdf
from PyPDF2 import PdfMerger
import os
from utils.drive_handler import upload_arquivo

def upload_pdf_drive(pasta_id, arquivo_local, nome_arquivo):
    """
    Faz upload de um PDF para o Google Drive
    """
    with open(arquivo_local, 'rb') as f:
        conteudo = f.read()
    return upload_arquivo(pasta_id, nome_arquivo, conteudo, 'application/pdf')

def converter_para_pdf(pasta_info, arquivos, nome_cliente):
    """
    Converte arquivos individuais para PDF e faz upload para o Drive
    """
    pdfs_gerados = []
    
    for arquivo_info in arquivos:
        if arquivo_info is None:
            continue
            
        arquivo = arquivo_info['content']
        arquivo_tipo = arquivo_info['type']
            
        # Determinar o tipo de documento
        if arquivo_tipo == 'comprovante_residencia':
            nome_arquivo = f"Comprovante de Residencia - {nome_cliente}.pdf"
        elif arquivo_tipo == 'documento_identidade':
            nome_arquivo = f"Documento de Identidade - {nome_cliente}.pdf"
        else:
            continue
            
        output_pdf = os.path.join(pasta_info['local'], nome_arquivo)
        temp_path = os.path.join(pasta_info['local'], f"temp_{arquivo.name}")
        
        try:
            # Salvar arquivo temporariamente
            with open(temp_path, "wb") as f:
                f.write(arquivo.getbuffer())
            
            if arquivo.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Converter imagem para PDF
                with Image.open(temp_path) as img:
                    img.save(output_pdf, "PDF")
            else:
                # Se já for PDF, apenas copiar
                with open(output_pdf, 'wb') as f:
                    f.write(arquivo.getbuffer())
            
            # Upload para o Drive
            file_id = upload_pdf_drive(pasta_info['drive_id'], output_pdf, nome_arquivo)
            pdfs_gerados.append({'local': output_pdf, 'drive_id': file_id})
            
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return pdfs_gerados

def combinar_comprovantes_gastos(pasta_info, arquivos_gastos, nome_cliente):
    """
    Combina múltiplos comprovantes de gastos em um único PDF
    """
    if not arquivos_gastos:
        return None
        
    output_path = os.path.join(pasta_info['local'], f"Comprovante de Gastos - {nome_cliente}.pdf")
    merger = PdfMerger()
    
    for arquivo in arquivos_gastos:
        temp_path = os.path.join(pasta_info['local'], f"temp_{arquivo.name}")
        pdf_path = os.path.splitext(temp_path)[0] + '.pdf'
        
        try:
            # Salvar arquivo temporariamente
            with open(temp_path, "wb") as f:
                f.write(arquivo.getbuffer())
            
            # Se for imagem, converter para PDF
            if arquivo.name.lower().endswith(('.png', '.jpg', '.jpeg')):
                with Image.open(temp_path) as img:
                    img.save(pdf_path, "PDF")
                merger.append(pdf_path)
            else:
                merger.append(temp_path)
                
        finally:
            # Limpar arquivos temporários
            try:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                if os.path.exists(pdf_path) and temp_path != pdf_path:
                    os.remove(pdf_path)
            except Exception as e:
                print(f"Erro ao remover arquivo temporário: {str(e)}")
    
    merger.write(output_path)
    merger.close()
    
    # Upload para o Drive
    file_id = upload_pdf_drive(pasta_info['drive_id'], output_path, f"Comprovante de Gastos - {nome_cliente}.pdf")
    
    return {'local': output_path, 'drive_id': file_id}

def combinar_todos_documentos(pasta_info, nome_cliente):
    """
    Combina todos os documentos em um único PDF
    """
    # Lista de nomes de arquivos na ordem desejada
    arquivos = [
        f"Comprovante de Residencia - {nome_cliente}.pdf",
        f"Documento de Identidade - {nome_cliente}.pdf",
        f"Comprovante de Gastos - {nome_cliente}.pdf"
    ]
    
    output_path = os.path.join(pasta_info['local'], f"Documentos Combinados - {nome_cliente}.pdf")
    merger = PdfMerger()
    
    # Adiciona cada documento na ordem especificada
    for arquivo in arquivos:
        arquivo_path = os.path.join(pasta_info['local'], arquivo)
        if os.path.exists(arquivo_path):
            merger.append(arquivo_path)
    
    merger.write(output_path)
    merger.close()
    
    # Upload para o Drive
    file_id = upload_pdf_drive(pasta_info['drive_id'], output_path, f"Documentos Combinados - {nome_cliente}.pdf")
    
    return {'local': output_path, 'drive_id': file_id} 