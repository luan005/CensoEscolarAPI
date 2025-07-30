import requests
import json

url = "https://servicodados.ibge.gov.br/api/v1/localidades/microrregioes"

try:
    response = requests.get(url)
    response.raise_for_status()
    dados = response.json()

    with open("Microrregioes_Brasil.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

    print("Arquivo 'Microrregioes_Brasil.json' gerado com sucesso.")

except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
except Exception as e:
    print(f"Erro inesperado: {e}")
