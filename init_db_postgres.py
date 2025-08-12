import psycopg2
import json
import os

def carregar_json(caminho):
    if not os.path.exists(caminho):
        print(f"Arquivo {caminho} não encontrado. Ignorando.")
        return []
    with open(caminho, encoding='utf-8') as f:
        return json.load(f)

try:
    conn = psycopg2.connect(
        dbname='censoescolar',
        user='postgres',
        password='123456',
        host='localhost',
        port='5432'
    )
    conn.autocommit = True
    cursor = conn.cursor()

    print("Iniciando inserção de UFs...")
    ufs = carregar_json('UFs_Brasil.json')
    for uf in ufs:
        try:
            cursor.execute('''
                INSERT INTO tb_uf (id, sigla, nome, regiao_id, regiao_nome)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            ''', (uf['id'], uf['sigla'], uf['nome'], uf['regiao']['id'], uf['regiao']['nome']))
        except Exception as e:
            print(f"Erro ao inserir UF: {uf}")
            print(e)

    print("Iniciando inserção de Mesorregiões...")
    mesorregioes = carregar_json('Mesorregioes_Brasil.json')
    for meso in mesorregioes:
        try:
            cursor.execute('''
                INSERT INTO tb_mesorregiao (
                    id, nome, uf_id, uf_nome, uf_sigla, regiao_id, regiao_nome, regiao_sigla
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            ''', (
                meso['id'], meso['nome'], meso['UF']['id'], meso['UF']['nome'], 
                meso['UF']['sigla'], meso['UF']['regiao']['id'], 
                meso['UF']['regiao']['nome'], meso['UF']['regiao']['sigla']
            ))
        except Exception as e:
            print(f"Erro ao inserir Mesorregião: {meso}")
            print(e)

    print("Iniciando inserção de Microrregiões...")
    microrregioes = carregar_json('Microrregioes_Brasil.json')
    for micro in microrregioes:
        try:
            cursor.execute('''
                INSERT INTO tb_microrregiao (
                    id, nome, mesorregiao_id, mesorregiao_nome, uf_id, uf_nome, uf_sigla,
                    regiao_id, regiao_nome, regiao_sigla
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            ''', (
                micro['id'], micro['nome'], micro['mesorregiao']['id'], micro['mesorregiao']['nome'],
                micro['mesorregiao']['UF']['id'], micro['mesorregiao']['UF']['nome'], micro['mesorregiao']['UF']['sigla'],
                micro['mesorregiao']['UF']['regiao']['id'], micro['mesorregiao']['UF']['regiao']['nome'], micro['mesorregiao']['UF']['regiao']['sigla']
            ))
        except Exception as e:
            print(f"Erro ao inserir Microrregião: {micro}")
            print(e)

    print("Iniciando inserção de Municípios...")
    municipios = carregar_json('Municipios_Brasil_ID.json')
    for m in municipios:
        try:
            micro = m.get('microrregiao')
            if micro is None:
                print(f"Município ignorado por falta de microrregião: {m['nome']} ({m['id']})")
                continue
            meso = micro['mesorregiao']
            uf = meso['UF']
            regiao = uf['regiao']
            cursor.execute('''
                INSERT INTO tb_municipio (
                    id, nome, microrregiao_id, microrregiao_nome,
                    mesorregiao_id, mesorregiao_nome,
                    uf_id, uf_nome, uf_sigla,
                    regiao_id, regiao_nome, regiao_sigla
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            ''', (
                m['id'], m['nome'],
                micro['id'], micro['nome'],
                meso['id'], meso['nome'],
                uf['id'], uf['nome'], uf['sigla'],
                regiao['id'], regiao['nome'], regiao['sigla']
            ))
        except Exception as e:
            print(f"Erro ao inserir Município: {m}")
            print(e)

    print("Iniciando inserção de Instituições...")
    instituicoes_2023 = carregar_json("instituicoes_censo_2023.json")
    instituicoes_2024 = carregar_json("instituicoes_censo_2024.json")
    instituicoes = instituicoes_2023 + instituicoes_2024
    inseridos = 0
    ignorados = 0

    for inst in instituicoes:
        try:
            qt_mat_bas = inst.get('QT_MAT_BAS') or "0"
            co_municipio = inst.get('CO_MUNICIPIO')

            if not co_municipio:
                ignorados += 1
                continue

            values = (
                inst.get('NU_ANO_CENSO', 2023,),
                inst.get('NO_REGIAO', ''),
                inst.get('SG_UF', ''),
                inst.get('NO_MUNICIPIO', ''),
                inst.get('NO_MESORREGIAO', ''),
                inst.get('NO_MICRORREGIAO', ''),
                inst.get('CO_ENTIDADE', ''),
                qt_mat_bas,
                inst.get('CO_REGIAO', ''),
                inst.get('CO_UF', ''),
                co_municipio,
                inst.get('CO_MICRORREGIAO', ''),
                inst.get('CO_MESORREGIAO', '')
            )

            cursor.execute('''
                INSERT INTO tb_instituicao (
                    nu_ano_censo, no_regiao, sg_uf, no_municipio, no_mesorregiao, no_microrregiao,
                    co_entidade, qt_mat_bas, co_regiao, co_uf, co_municipio, co_microrregiao, co_mesorregiao
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            ''', values)
            inseridos += 1

        except Exception as e:
            ignorados += 1
            print(f"Erro ao inserir Instituição: {inst}")
            print(e)

    print(f"{inseridos} instituições inseridas com sucesso. {ignorados} ignoradas.")

    cursor.close()
    conn.close()
    print("Carga finalizada com sucesso.")

except Exception as e:
    print(f"Erro geral: {e}")