import sqlite3
import json
import os


def carregar_json(caminho):
    if not os.path.exists(caminho):
        print(f"Arquivo {caminho} não encontrado. Ignorando.")
        return []
    with open(caminho, encoding='utf-8') as f:
        return json.load(f)


def criar_tabelas(cursor):
    with open("schemas.sql", "r", encoding="utf-8") as f:
        schema = f.read()
        cursor.executescript(schema)
    print("Tabelas criadas ou já existentes.")


def inserir_ufs(cursor):
    ufs = carregar_json('UF_Nordeste.json')
    for uf in ufs:
        cursor.execute('''
            INSERT OR IGNORE INTO tb_uf (id, sigla, nome, regiao_id, regiao_nome)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            uf['id'],
            uf['sigla'],
            uf['nome'],
            uf['regiao']['id'],
            uf['regiao']['nome']
        ))
    print("UFs inseridas com sucesso.")

def inserir_mesorregioes(cursor):
    mesorregioes = carregar_json('Mesorregioes_Nordeste.json')
    for meso in mesorregioes:
        cursor.execute('''
            INSERT OR IGNORE INTO tb_mesorregiao (
                id, nome, uf_id, uf_nome, uf_sigla,
                regiao_id, regiao_nome, regiao_sigla
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            meso['id'],
            meso['nome'],
            meso['UF']['id'],
            meso['UF']['nome'],
            meso['UF']['sigla'],
            meso['UF']['regiao']['id'],
            meso['UF']['regiao']['nome'],
            meso['UF']['regiao']['sigla']
        ))
    print("Mesorregiões inseridas com sucesso.")

def inserir_microrregioes(cursor):
    microrregioes = carregar_json('Microrregioes_Nordeste.json')
    for micro in microrregioes:
        cursor.execute('''
            INSERT OR IGNORE INTO tb_microrregiao (
                id, nome, mesorregiao_id, mesorregiao_nome,
                uf_id, uf_nome, uf_sigla,
                regiao_id, regiao_nome, regiao_sigla
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            micro['id'],
            micro['nome'],
            micro['mesorregiao']['id'],
            micro['mesorregiao']['nome'],
            micro['mesorregiao']['UF']['id'],
            micro['mesorregiao']['UF']['nome'],
            micro['mesorregiao']['UF']['sigla'],
            micro['mesorregiao']['UF']['regiao']['id'],
            micro['mesorregiao']['UF']['regiao']['nome'],
            micro['mesorregiao']['UF']['regiao']['sigla']
        ))
    print("Microrregiões inseridas com sucesso.")

def inserir_municipios(cursor):
    municipios = carregar_json('Municipios_Nordeste_ID.json')
    for m in municipios:
        micro = m['microrregiao']
        meso = micro['mesorregiao']
        uf = meso['UF']
        regiao = uf['regiao']
        cursor.execute('''
            INSERT OR IGNORE INTO tb_municipio (
                id, nome, microrregiao_id, microrregiao_nome,
                mesorregiao_id, mesorregiao_nome,
                uf_id, uf_nome, uf_sigla,
                regiao_id, regiao_nome, regiao_sigla
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            m['id'],
            m['nome'],
            micro['id'],
            micro['nome'],
            meso['id'],
            meso['nome'],
            uf['id'],
            uf['nome'],
            uf['sigla'],
            regiao['id'],
            regiao['nome'],
            regiao['sigla']
        ))
    print("Municípios inseridos com sucesso.")

def inserir_instituicoes(cursor):
    instituicoes = carregar_json('dados_nordeste.json')
    inseridos = 0
    ignorados = 0

    for inst in instituicoes:
        try:
            qt_mat_bas = inst.get('QT_MAT_BAS') or "0"
            values = (
                inst.get('NO_REGIAO', ''),
                inst.get('SG_UF', ''),
                inst.get('NO_MUNICIPIO', ''),
                inst.get('NO_MESORREGIAO', ''),
                inst.get('NO_MICRORREGIAO', ''),
                inst.get('CO_ENTIDADE', ''),
                qt_mat_bas,
                inst.get('CO_REGIAO', ''),
                inst.get('CO_UF', ''),
                inst.get('CO_MUNICIPIO', ''),
                inst.get('CO_MICRORREGIAO', ''),
                inst.get('CO_MESORREGIAO', '')
            )
            cursor.execute('''
                INSERT OR IGNORE INTO tb_instituicao (
                    no_regiao, sg_uf, no_municipio, no_mesorregiao, no_microrregiao,
                    co_entidade, qt_mat_bas, co_regiao, co_uf, co_municipio,
                    co_microrregiao, co_mesorregiao
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', values)
            inseridos += 1
        except Exception as e:
            ignorados += 1
            print(f"Erro Instituição: {e} - {inst.get('CO_ENTIDADE')}")

    print(f"{inseridos} instituições inseridas com sucesso. {ignorados} ignoradas.")

def main():
    conn = sqlite3.connect('censoescolar.db')
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    try:
        criar_tabelas(cursor)
        inserir_ufs(cursor)
        inserir_mesorregioes(cursor)
        inserir_microrregioes(cursor)
        inserir_municipios(cursor)
        inserir_instituicoes(cursor)
    except Exception as e:
        print(f"Erro geral: {e}")
    finally:
        conn.commit()
        conn.close()
        print("Inserção completa de todos os dados.")

if __name__ == "__main__":
    main()
