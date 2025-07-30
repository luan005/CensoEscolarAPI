import pandas as pd
import json

# Caminho do arquivo CSV de entrada
input_csv = 'microdados_ed_basica_2024.csv'

# Campos que você quer extrair
columns_to_extract = [
    "NU_ANO_CENSO",
    "NO_REGIAO",
    "CO_REGIAO",
    "SG_UF",
    "CO_UF",
    "NO_MUNICIPIO",
    "CO_MUNICIPIO",
    "NO_ENTIDADE",
    "CO_ENTIDADE",
    "QT_MAT_BAS"
]

try:
    # Lê apenas as colunas necessárias (corrigindo encoding típico do Censo Escolar)
    df = pd.read_csv(input_csv, sep=';', usecols=columns_to_extract, encoding='ISO-8859-1')

    # Opcional: Remover linhas duplicadas
    df = df.drop_duplicates()

    # Opcional: Remover registros com CO_ENTIDADE nulo
    df = df[df['CO_ENTIDADE'].notnull()]

    # Salvar em JSON
    output_json = 'instituicoes_censo_2024.json'
    df.to_json(output_json, orient='records', force_ascii=False, indent=4)

    print(f"Arquivo JSON salvo com sucesso em: {output_json}")

except Exception as e:
    print(f"Erro durante a extração: {e}")
