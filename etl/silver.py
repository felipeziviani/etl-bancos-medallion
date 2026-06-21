import pandas as pd
import os

DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "data"))

CAMINHO_ENTRADA = os.path.join(DATA_DIR, "bronze", "bancos.parquet")
CAMINHO_SAIDA = os.path.join(DATA_DIR, "silver", "bancos_silver.parquet")

def executar_silver():
    print(f"\nCarregando dados do arquivo: {CAMINHO_ENTRADA}")
    df = pd.read_parquet(CAMINHO_ENTRADA)

    linhas_antes = len(df)
    
    df = df.dropna(subset=["code"])
    df = df.drop_duplicates(subset=["code"])

    df["name"] = df["name"].str.strip()
    df["fullName"] = df["fullName"].str.strip()

    df = df[df["name"] != ""]
    df["code"] = df["code"].astype(int)

    df = df.rename(columns={
        "name": "nome_curto",
        "fullName": "nome_completo",
        "code": "codigo_banco",
        "ispb": "ispb",
    })

    df["data_coleta"] = pd.to_datetime(df["data_coleta"])

    linhas_depois = len(df)
    print(f"\nLinhas antes: {linhas_antes}")
    print(f"Linhas depois: {linhas_depois}")
    print(f"Linhas removidas: {linhas_antes - linhas_depois}" )

    print(df.head())

    os.makedirs(os.path.dirname(CAMINHO_SAIDA), exist_ok=True)
    df.to_parquet(CAMINHO_SAIDA, index=False)
    print(f"\nArquivo salvo em: {CAMINHO_SAIDA}")
    
    return df

if __name__ == "__main__":
    executar_silver()