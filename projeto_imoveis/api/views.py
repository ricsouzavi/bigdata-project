# api/views.py
# api/views.py
import json
import pandas as pd
from django.http import JsonResponse, HttpResponseNotFound
import unicodedata

# ... (O resto do topo do arquivo fica igual) ...

DADOS_EVOLUCAO_ANO = []
DADOS_PRECO_BAIRRO = []
DF_DADOS_COMPLETOS = pd.DataFrame()

def carregar_dados():
    global DADOS_EVOLUCAO_ANO, DADOS_PRECO_BAIRRO, DF_DADOS_COMPLETOS
    try:
        with open("dados_api_ano.json", "r") as f:
            DADOS_EVOLUCAO_ANO = json.load(f)
        print("Dados de 'evolucao por ano' carregados.")

        with open("dados_api_bairro.json", "r") as f:
            DADOS_PRECO_BAIRRO = json.load(f)
        print("Dados de 'preco por bairro' carregados.")

        # --- A CORREÇÃO ESTÁ AQUI ---
        DF_DADOS_COMPLETOS = pd.read_csv("datasetsimul.csv")
        
        # 1. Força a coluna 'ano' a ser numérica.
        #    'errors='coerce'' transforma erros (como "2Good") em "Nulo" (NaT/NaN)
        DF_DADOS_COMPLETOS['ano'] = pd.to_numeric(DF_DADOS_COMPLETOS['ano'], errors='coerce')
        
        # 2. (Opcional, mas bom) Remove as linhas que tinham anos inválidos
        DF_DADOS_COMPLETOS = DF_DADOS_COMPLETOS.dropna(subset=['ano'])
        
        # 3. Converte de float (ex: 2020.0) para inteiro (ex: 2020)
        DF_DADOS_COMPLETOS['ano'] = DF_DADOS_COMPLETOS['ano'].astype(int)
        
        print("Dataset completo 'datasetsimul.csv' carregado e coluna 'ano' limpa.")
        
    except FileNotFoundError:
        print("ERRO: Arquivos de dados (.json ou .csv) não encontrados.")
        print("Rode 'python manage.py processar_dados' primeiro.")
    except Exception as e:
        print(f"Erro inesperado ao carregar dados: {e}")
        
# Carrega os dados uma vez quando o Django inicia
carregar_dados()

# --- Endpoints da API ---

def get_evolucao_por_ano(request):
    """
    Retorna a média de preço agrupada por ano.
    """
    if not DADOS_EVOLUCAO_ANO:
        return JsonResponse({"erro": "Dados não carregados"}, status=500)
    return JsonResponse(DADOS_EVOLUCAO_ANO, safe=False)

def get_preco_por_bairro(request):
    """
    Retorna a média de preço do último ano agrupada por bairro.
    """
    if not DADOS_PRECO_BAIRRO:
        return JsonResponse({"erro": "Dados não carregados"}, status=500)
    return JsonResponse(DADOS_PRECO_BAIRRO, safe=False)

def get_dados_filtrados(request):
    """
    Filtra o dataset completo com base nos parâmetros de query.
    """
    if DF_DADOS_COMPLETOS.empty:
        return JsonResponse({"erro": "Dataset de filtros não carregado"}, status=500)
        
    df_filtrado = DF_DADOS_COMPLETOS.copy()
    
    # Pega os query parameters
    ano_str = request.GET.get('ano')
    bairro = request.GET.get('bairro')
    
    try:
        if ano_str:
            ano = int(ano_str)
            df_filtrado = df_filtrado[df_filtrado['ano'] == ano]
        if bairro:
            df_filtrado = df_filtrado[df_filtrado['bairro'] == bairro]
    except ValueError:
        return JsonResponse({"erro": "Ano inválido"}, status=400)
        
    # Converte o resultado para JSON e retorna
    dados_json = df_filtrado.to_dict("records")
    return JsonResponse(dados_json, safe=False)