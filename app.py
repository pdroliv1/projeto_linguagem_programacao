"""Dashboard de acidentes de trânsito no Brasil (base simulada)."""
from pathlib import Path
import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from sqlalchemy import create_engine

st.set_page_config(page_title="Radar de Segurança Viária", page_icon="RV", layout="wide")

st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #123047 0%, #0b1f30 100%);
        border-right: 1px solid #285269;
    }
    [data-testid="stSidebar"] > div:first-child {
        padding: 1.5rem 1rem;
    }
    [data-testid="stSidebar"] h3 {
        color: #f7c873;
        letter-spacing: 0.04em;
        margin-bottom: 0.2rem;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #b7cedb;
        font-size: 0.82rem;
        margin-bottom: 1.25rem;
    }
    [data-testid="stSidebar"] [data-testid="stMultiSelect"] {
        background: rgba(255, 255, 255, 0.07);
        border: 1px solid rgba(183, 206, 219, 0.25);
        border-left: 4px solid #f7c873;
        border-radius: 10px;
        margin-bottom: 0.9rem;
        padding: 0.4rem 0.5rem 0.15rem;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] {
        background-color: #1f6f78 !important;
        border-radius: 5px !important;
    }
    [data-testid="stSidebar"] [data-baseweb="tag"] span {
        color: #ffffff !important;
        font-weight: 600;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] > div {
        background-color: transparent !important;
        border: 0 !important;
    }
</style>
""", unsafe_allow_html=True)

ROOT = Path(__file__).parent
DATA_PATH = ROOT / "dados" / "acidentes_transito_brasil.csv"
DB_PATH = ROOT / "database" / "acidentes.db"

@st.cache_data
def carregar_dados(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, encoding="utf-8")
    df["data"] = pd.to_datetime(df["data"])
    df["periodo"] = df["data"].dt.to_period("M").astype(str)
    df["taxa_mortalidade"] = np.where(df["acidentes"] > 0, df["mortes"] / df["acidentes"] * 100, 0)
    df["indice_vitimas"] = df["feridos"] + df["mortes"]
    return df

def persistir_sqlite(df: pd.DataFrame) -> None:
    """Mantém uma cópia consultável da base tratada em SQLite via SQLAlchemy."""
    DB_PATH.parent.mkdir(exist_ok=True)
    engine = create_engine(f"sqlite:///{DB_PATH.as_posix()}")
    df.to_sql("acidentes", engine, if_exists="replace", index=False)

df = carregar_dados(str(DATA_PATH))
persistir_sqlite(df)

st.title("Radar de Segurança Viária no Brasil")
st.markdown("""**Disciplina:** Linguagens de programação

**Professor:** Alexandre Neves Louzada

**Aluno:** Pedro Rigo de Oliveira""")
st.caption("Análise exploratória de dados simulados de acidentes de trânsito — 2015 a 2024")
st.info("Esta aplicação usa uma base simulada para fins educacionais. Os resultados indicam padrões do conjunto de dados, não estatísticas oficiais.")

with st.sidebar:
    st.markdown("### Painel de filtros")
    st.caption("Ajuste o recorte da análise em cada dimensão.")
    anos = st.multiselect("Ano", sorted(df["ano"].unique()), default=sorted(df["ano"].unique()))
    regioes = st.multiselect("Região", sorted(df["regiao"].unique()), default=sorted(df["regiao"].unique()))
    ufs_disponiveis = sorted(df.loc[df["regiao"].isin(regioes), "uf"].unique())
    ufs = st.multiselect("UF", ufs_disponiveis, default=ufs_disponiveis)
    gravidades = st.multiselect("Gravidade", sorted(df["nivel_gravidade"].unique()), default=sorted(df["nivel_gravidade"].unique()))
    tipos = st.multiselect("Tipo de acidente", sorted(df["tipo_acidente"].unique()), default=sorted(df["tipo_acidente"].unique()))

filtrado = df[df["ano"].isin(anos) & df["regiao"].isin(regioes) & df["uf"].isin(ufs) & df["nivel_gravidade"].isin(gravidades) & df["tipo_acidente"].isin(tipos)].copy()
if filtrado.empty:
    st.warning("Nenhum registro atende aos filtros selecionados.")
    st.stop()

total_acidentes = int(filtrado["acidentes"].sum())
total_mortes = int(filtrado["mortes"].sum())
total_feridos = int(filtrado["feridos"].sum())
taxa = total_mortes / total_acidentes * 100 if total_acidentes else 0
c1, c2, c3, c4 = st.columns(4)
c1.metric("Acidentes", f"{total_acidentes:,.0f}".replace(",", "."))
c2.metric("Mortes", f"{total_mortes:,.0f}".replace(",", "."))
c3.metric("Feridos", f"{total_feridos:,.0f}".replace(",", "."))
c4.metric("Mortalidade", f"{taxa:.2f}%")

tab1, tab2, tab3, tab4 = st.tabs(["Visão geral", "Tempo", "Geografia", "Dados e método"])
with tab1:
    col1, col2 = st.columns(2)
    por_regiao = filtrado.groupby("regiao", as_index=False).agg(acidentes=("acidentes", "sum"), mortes=("mortes", "sum"))
    por_regiao["taxa_mortalidade"] = por_regiao["mortes"] / por_regiao["acidentes"] * 100
    fig_regiao = px.bar(por_regiao.sort_values("acidentes"), x="acidentes", y="regiao", orientation="h", color="regiao", title="Volume de acidentes por região", labels={"acidentes": "Acidentes", "regiao": "Região"})
    col1.plotly_chart(fig_regiao, use_container_width=True)
    por_tipo = filtrado.groupby("tipo_acidente", as_index=False)["acidentes"].sum().sort_values("acidentes", ascending=False)
    col2.plotly_chart(px.pie(por_tipo, values="acidentes", names="tipo_acidente", hole=.45, title="Composição por tipo de acidente"), use_container_width=True)
    st.subheader("Gravidade e condições de visibilidade")
    cruzamento = pd.crosstab(filtrado["visibilidade"], filtrado["nivel_gravidade"], values=filtrado["acidentes"], aggfunc="sum").fillna(0)
    st.plotly_chart(px.imshow(cruzamento, text_auto=".0f", color_continuous_scale="YlOrRd", labels=dict(x="Gravidade", y="Visibilidade", color="Acidentes")), use_container_width=True)

with tab2:
    mensal = filtrado.groupby("periodo", as_index=False).agg(acidentes=("acidentes", "sum"), mortes=("mortes", "sum"), feridos=("feridos", "sum"))
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=mensal["periodo"], y=mensal["acidentes"], name="Acidentes", mode="lines+markers"))
    fig.add_trace(go.Scatter(x=mensal["periodo"], y=mensal["mortes"], name="Mortes", mode="lines+markers", yaxis="y2"))
    fig.update_layout(title="Evolução mensal", yaxis=dict(title="Acidentes"), yaxis2=dict(title="Mortes", overlaying="y", side="right"), hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)
    por_mes = filtrado.groupby("mes", as_index=False)["acidentes"].sum()
    st.plotly_chart(px.bar(por_mes, x="mes", y="acidentes", title="Sazonalidade: acidentes por mês", labels={"mes": "Mês", "acidentes": "Acidentes"}), use_container_width=True)

with tab3:
    por_uf = filtrado.groupby(["uf", "regiao"], as_index=False).agg(acidentes=("acidentes", "sum"), mortes=("mortes", "sum"), feridos=("feridos", "sum"))
    por_uf["mortalidade"] = por_uf["mortes"] / por_uf["acidentes"] * 100
    st.plotly_chart(px.scatter(por_uf, x="acidentes", y="mortes", size="feridos", color="regiao", hover_name="uf", title="Comparação entre UFs", labels={"acidentes": "Acidentes", "mortes": "Mortes"}), use_container_width=True)
    st.dataframe(por_uf.sort_values("mortes", ascending=False), use_container_width=True, hide_index=True)

with tab4:
    st.subheader("Base, tratamento e integração")
    st.write("A fonte é o CSV fornecido para a avaliação. A aplicação converte datas, cria período mensal, índice de vítimas e taxa de mortalidade. Uma cópia tratada é persistida com SQLAlchemy e SQLite em database/acidentes.db a cada execução.")
    st.subheader("Recorte filtrado")
    st.dataframe(filtrado.sort_values("data", ascending=False), use_container_width=True, hide_index=True)
    st.download_button("Baixar dados filtrados (CSV)", filtrado.to_csv(index=False).encode("utf-8"), "acidentes_filtrados.csv", "text/csv")
    st.subheader("Conclusão executiva")
    lider = por_regiao.sort_values("acidentes", ascending=False).iloc[0]
    st.write(f"No recorte atual, {lider['regiao']} concentra o maior volume de acidentes ({lider['acidentes']:,.0f}). A taxa de mortalidade consolidada é de {taxa:.2f}%. Use os filtros para priorizar regiões, UFs e condições associadas a maior gravidade.")
