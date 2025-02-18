from supabase import create_client
import os
import streamlit as st

# Configurações do Supabase
SUPABASE_URL = "https://bskykszrjuxvqxgngnir.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJza3lrc3pyanV4dnF4Z25nbmlyIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzgyNTM1MTQsImV4cCI6MjA1MzgyOTUxNH0.kFHRv-omueUwKlhwjWDleJe27fgmlYA4myoxlKRsgQg"

def get_supabase_client():
    """
    Cria e retorna um cliente do Supabase
    """
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return supabase
    except Exception as e:
        raise Exception(f"Erro ao conectar com Supabase: {str(e)}")

def salvar_cliente(dados_cliente):
    """
    Salva os dados do cliente na tabela Clientes_Ativos_SmartLegal
    """
    try:
        supabase = get_supabase_client()
        
        # Preparar dados para inserção
        cliente_data = {
            'nome': dados_cliente['nome'],
            'nacionalidade': dados_cliente['nacionalidade'],
            'estado_civil': dados_cliente['estado_civil'],
            'profissao': dados_cliente['profissao'],
            'email': dados_cliente['email'],
            'celular': dados_cliente['celular'],
            'data_nascimento': dados_cliente['data_nascimento'],
            'rg': dados_cliente['rg'],
            'cpf': dados_cliente['cpf'],
            'rua': dados_cliente['rua'],
            'bairro': dados_cliente['bairro'],
            'complemento': dados_cliente['complemento'],
            'cep': dados_cliente['cep'],
            'cidade': dados_cliente['cidade'],
            'estado': dados_cliente['estado']
        }
        
        # Inserir no Supabase
        response = supabase.table('Clientes_Ativos_SmartLegal').insert(cliente_data).execute()
        
        if not response.data:
            raise Exception("Nenhum dado retornado após a inserção")
            
        return response.data[0]['id']  # Retorna o ID do cliente inserido
        
    except Exception as e:
        raise Exception(f"Erro ao salvar cliente no banco de dados: {str(e)}")

def listar_clientes():
    """
    Lista todos os clientes ordenados por nome
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table('Clientes_Ativos_SmartLegal').select('*').order('nome').execute()
        return response.data
    except Exception as e:
        raise Exception(f"Erro ao listar clientes: {str(e)}")

def buscar_cliente_por_cpf(cpf):
    """
    Busca um cliente específico pelo CPF
    """
    try:
        supabase = get_supabase_client()
        response = supabase.table('Clientes_Ativos_SmartLegal').select('*').eq('cpf', cpf).execute()
        return response.data[0] if response.data else None
    except Exception as e:
        raise Exception(f"Erro ao buscar cliente: {str(e)}") 