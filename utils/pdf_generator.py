from PIL import Image
import img2pdf
from PyPDF2 import PdfMerger
import os

def converter_para_pdf(pasta_cliente, arquivos, nome_cliente):
    """
    Converte arquivos individuais para PDF
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
            continue  # Ignora outros tipos de arquivo
            
        output_pdf = os.path.join(pasta_cliente, nome_arquivo)
        temp_path = os.path.join(pasta_cliente, f"temp_{arquivo.name}")
        
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
            
            pdfs_gerados.append(output_pdf)
            
        finally:
            # Limpar arquivo temporário
            if os.path.exists(temp_path):
                os.remove(temp_path)
    
    return pdfs_gerados

def combinar_comprovantes_gastos(pasta_cliente, arquivos_gastos, nome_cliente):
    """
    Combina múltiplos comprovantes de gastos em um único PDF
    """
    if not arquivos_gastos:
        return None
        
    output_path = os.path.join(pasta_cliente, f"Comprovante de Gastos - {nome_cliente}.pdf")
    merger = PdfMerger()
    
    for arquivo in arquivos_gastos:
        temp_path = os.path.join(pasta_cliente, f"temp_{arquivo.name}")
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
    
    # Limpar quaisquer arquivos temporários remanescentes
    for arquivo in os.listdir(pasta_cliente):
        if arquivo.startswith('temp_'):
            try:
                os.remove(os.path.join(pasta_cliente, arquivo))
            except Exception as e:
                print(f"Erro ao remover arquivo temporário: {str(e)}")
    
    return output_path

def combinar_todos_documentos(pasta_cliente, nome_cliente):
    """
    Combina todos os documentos em um único PDF
    """
    # Lista de nomes de arquivos na ordem desejada
    arquivos = [
        f"Comprovante de Residencia - {nome_cliente}.pdf",
        f"Documento de Identidade - {nome_cliente}.pdf",
        f"Comprovante de Gastos - {nome_cliente}.pdf"
    ]
    
    output_path = os.path.join(pasta_cliente, f"Documentos Combinados - {nome_cliente}.pdf")
    merger = PdfMerger()
    
    # Adiciona cada documento na ordem especificada
    for arquivo in arquivos:
        arquivo_path = os.path.join(pasta_cliente, arquivo)
        if os.path.exists(arquivo_path):
            merger.append(arquivo_path)
    
    merger.write(output_path)
    merger.close()
    
    # Limpar quaisquer arquivos temporários remanescentes
    for arquivo in os.listdir(pasta_cliente):
        if arquivo.startswith('temp_'):
            try:
                os.remove(os.path.join(pasta_cliente, arquivo))
            except Exception as e:
                print(f"Erro ao remover arquivo temporário: {str(e)}")
    
    return output_path 