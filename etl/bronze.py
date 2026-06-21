import time
import requests
import pandas as pd
from datetime import datetime
import os


URL_BANCOS = "https://brasilapi.com.br/api/banks/v1"
DATA_DIR = os.getenv("DATA_DIR", os.path.join(
    os.path.dirname(__file__), "..", "data"))
CAMINHO_SAIDA = os.path.join(DATA_DIR, "bronze", "bancos.parquet")

MAX_TENTATIVAS = 3
ESPERA_SEGUNDOS = 5


def buscar_bancos() -> list:
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        print(
            f"Buscando lista de bancos... (tentativa {tentativa}/{MAX_TENTATIVAS})")
        try:
            response = requests.get(URL_BANCOS, timeout=15)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as erro:
            print(f"Erro HTTP: {erro}")

        except requests.exceptions.RequestException as erro:
            print(f"Erro na requisição: {erro}")

        if tentativa < MAX_TENTATIVAS:
            print(
                f"Aguardando {ESPERA_SEGUNDOS} segundos antes da próxima tentativa...")
            time.sleep(ESPERA_SEGUNDOS)

    print(
        f"Não foi possível obter a lista de bancos após {MAX_TENTATIVAS} tentativas.")
    return []


def executar_bronze():
    bancos = buscar_bancos()

    if not bancos:
        print("\nNenhum banco foi coletado. A API pode estar indisponível.")
        return pd.DataFrame()
    data_coleta = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for banco in bancos:
        banco["data_coleta"] = data_coleta
    df = pd.DataFrame(bancos)
    print(f"\nTotal de bancos coletados: {len(df)}")
    print(df.head())

    os.makedirs(os.path.dirname(CAMINHO_SAIDA), exist_ok=True)

    df.to_parquet(CAMINHO_SAIDA, index=False)
    print(f"\nArquivo salvo em: {CAMINHO_SAIDA}")
    return df


if __name__ == "__main__":
    executar_bronze()
