import pandas as pd
import os

DATA_DIR = os.getenv("DATA_DIR", os.path.join(os.path.dirname(__file__), "..", "data"))
CAMINHO_ENTRADA = os.path.join(DATA_DIR, "silver", "bancos_silver.parquet")
CAMINHO_SAIDA = os.path.join(DATA_DIR, "gold", "bancos_gold.parquet")

def classificar_tipo_instituicao(nome_completo: str) -> str:
    
    nome = nome_completo.upper()

    if "COOPERATIVA" in nome or "COOP" in nome:
        return "Cooperativa de Crédito"
    elif "S.A." in nome or "S/A" in nome:
        return "Sociedade Anônima"
    elif "LTDA" in nome:
        return "Sociedade Limitada"
    else:
        return "Outros"

def executar_gold():
    print(f"\nLendo dados de: {CAMINHO_ENTRADA}")
    df = pd.read_parquet(CAMINHO_ENTRADA)

    df["tipo_instituicao"] = df["nome_completo"].apply(classificar_tipo_instituicao)

    resumo = (
        df.groupby("tipo_instituicao")["codigo_banco"]
        .count()
        .reset_index()
        .rename(columns={"codigo_banco": "quantidade_bancos"})
    )

    resumo = resumo.sort_values("quantidade_bancos", ascending=False)

    print("\nResumo final:")
    print(resumo)

    os.makedirs(os.path.dirname(CAMINHO_SAIDA), exist_ok=True)
    resumo.to_parquet(CAMINHO_SAIDA, index=False)
    print(f"\nArquivo salvo em: {CAMINHO_SAIDA}")

    return resumo

if __name__ == "__main__":
    executar_gold()