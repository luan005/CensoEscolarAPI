import requests
import json

url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"

response = requests.get(url)
municipios = response.json()

with open("Municipios_Brasil_ID.json", "w", encoding="utf-8") as f:
    json.dump(municipios, f, ensure_ascii=False, indent=4)

print("Municipios_Brasil_ID.json gerado com sucesso.")
