from etl.bronze import executar_bronze
from etl.silver import executar_silver
from etl.gold import executar_gold


def main():
    print("=" * 50)
    print("INICIANDO PIPELINE ETL - BANCOS BRASIL")
    print("=" * 50)

    print("\n--- Etapa 1: BRONZE ---")
    executar_bronze()

    print("\n--- Etapa 2: SILVER ---")
    executar_silver()

    print("\n--- Etapa 3: GOLD ---")
    executar_gold()

    print("\n" + "=" * 50)
    print("PIPELINE CONCLUÍDO")
    print("=" * 50)


if __name__ == "__main__":
    main()