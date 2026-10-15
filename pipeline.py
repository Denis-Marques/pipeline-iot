
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
CSV_PATH = "data/IOT-temp.csv"


def processar_dados():
    print("Lendo arquivo CSV...")
    df = pd.read_csv(CSV_PATH)

    df.columns = ["id", "room_id", "noted_date", "temp", "out_in"]

    df["noted_date"] = pd.to_datetime(
        df["noted_date"],
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )
    df["temp"] = pd.to_numeric(df["temp"], errors="coerce")
    df = df.dropna(subset=["id", "noted_date", "temp"])
    df = df.drop_duplicates(subset=["id"])

    print(f"Registros válidos: {len(df)}")

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL não foi definida no arquivo .env")

    print("Conectando ao PostgreSQL...")
    engine = create_engine(DATABASE_URL)

    try:
        df.to_sql(
            "leituras_temperatura",
            engine,
            if_exists="replace",
            index=False,
            chunksize=5000,
            method="multi"
        )

        print("Dados armazenados com sucesso!")

        with engine.connect() as conexao:
            total = conexao.execute(
                text("SELECT COUNT(*) FROM leituras_temperatura")
            ).scalar_one()
            print(f"Registros no PostgreSQL: {total}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    processar_dados()
