# api/management/commands/processar_dados.py
import pandas as pd
from django.core.management.base import BaseCommand

# O nome do seu novo arquivo CSV
ARQUIVO_CSV = "datasetsimul.csv" 

class Command(BaseCommand):
    help = 'Processa o CSV de imóveis e salva os arquivos JSON para a API'

    def handle(self, *args, **options):
        self.stdout.write("Iniciando processamento de dados com Pandas...")

        try:
            # 1. Carrega o dataset com Pandas
            df = pd.read_csv(ARQUIVO_CSV)

            # 2. Converte colunas para numérico (boa prática)
            df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
            df['ano'] = pd.to_numeric(df['ano'], errors='coerce')
            df = df.dropna(subset=['preco', 'ano']) # Limpa dados nulos

            # 3. Análise 1: Evolução por Ano (Substituindo PySpark)
            df_evolucao_ano = df.groupby('ano')['preco'].mean().reset_index()
            df_evolucao_ano = df_evolucao_ano.rename(columns={'preco': 'preco_medio'})

            # 4. Salva o JSON 1
            df_evolucao_ano.to_json("dados_api_ano.json", orient="records")
            self.stdout.write("... 'dados_api_ano.json' salvo com sucesso.")

            # 5. Análise 2: Média por Bairro (no último ano)
            ultimo_ano = df['ano'].max()
            df_bairros = df[df['ano'] == ultimo_ano]
            df_bairros_agg = df_bairros.groupby('bairro')['preco'].mean().reset_index()
            df_bairros_agg = df_bairros_agg.rename(columns={'preco': 'preco_medio_ultimo_ano'})
            df_bairros_agg = df_bairros_agg.sort_values(by='preco_medio_ultimo_ano', ascending=False)

            # 6. Salva o JSON 2
            df_bairros_agg.to_json("dados_api_bairro.json", orient="records")
            self.stdout.write("... 'dados_api_bairro.json' salvo com sucesso.")

            self.stdout.write(self.style.SUCCESS('Processamento concluído!'))

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"Erro: Arquivo '{ARQUIVO_CSV}' não encontrado."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erro inesperado: {e}"))