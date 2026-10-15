
import os
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")


st.set_page_config(
    page_title="Monitoramento IoT",
    page_icon="🌡️",
    layout="wide",
)

st.title("🌡️ Monitoramento de Temperatura IoT")
st.caption("Dashboard de análise das leituras armazenadas no PostgreSQL")

@st.cache_data(ttl=60)
def carregar_dados():
    engine = create_engine(DATABASE_URL)
    try:
        query = """
            SELECT id, room_id, noted_date, temp, out_in
            FROM leituras_temperatura
        """
        return pd.read_sql(query, engine)
    finally:
        engine.dispose()

try:
    df = carregar_dados()

    df["noted_date"] = pd.to_datetime(df["noted_date"])
    df["temp"] = pd.to_numeric(df["temp"])

    # Indicadores principais
    total = len(df)
    media = df["temp"].mean()
    minima = df["temp"].min()
    maxima = df["temp"].max()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total de leituras", f"{total:,}".replace(",", "."))
    c2.metric("Temperatura média", f"{media:.2f} °C")
    c3.metric("Temperatura mínima", f"{minima:.2f} °C")
    c4.metric("Temperatura máxima", f"{maxima:.2f} °C")

    st.divider()

    # Filtros
    st.subheader("Filtros")

    ambientes = sorted(df["out_in"].dropna().unique().tolist())
    selecionados = st.multiselect(
        "Tipo de ambiente",
        options=ambientes,
        default=ambientes,
    )

    filtrado = df[df["out_in"].isin(selecionados)].copy()

    if filtrado.empty:
        st.warning("Não há dados para os filtros selecionados.")
    else:
        # Gráfico da temperatura ao longo do tempo
        st.subheader("Temperatura ao longo do tempo")

        diario = (
            filtrado.assign(
                data=filtrado["noted_date"].dt.date
            )
            .groupby("data", as_index=False)["temp"]
            .mean()
        )

        fig_tempo = px.line(
            diario,
            x="data",
            y="temp",
            markers=True,
            labels={
                "data": "Data",
                "temp": "Temperatura média (°C)",
            },
            title="Média diária de temperatura",
        )
        st.plotly_chart(fig_tempo, use_container_width=True)

        # Comparação por ambiente
        st.subheader("Comparação entre ambientes")

        comparacao = (
            filtrado.groupby("out_in", as_index=False)["temp"]
            .mean()
        )

        fig_ambiente = px.bar(
            comparacao,
            x="out_in",
            y="temp",
            labels={
                "out_in": "Ambiente",
                "temp": "Temperatura média (°C)",
            },
            title="Temperatura média por tipo de ambiente",
        )
        st.plotly_chart(fig_ambiente, use_container_width=True)

        # Tabela de dados
        st.subheader("Últimas leituras registradas")

        recentes = filtrado.sort_values(
            "noted_date", ascending=False
        ).head(100)

        st.dataframe(
            recentes,
            use_container_width=True,
            hide_index=True,
        )

except Exception as erro:
    st.error("Não foi possível carregar os dados do PostgreSQL.")
    st.code(str(erro))
    st.info(
        "Confira se o contêiner postgres-iot está em execução "
        "e se a configuração de conexão está correta."
    )
