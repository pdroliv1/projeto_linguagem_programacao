# Radar de Segurança Viária no Brasil

Projeto da Avaliação G1 de Análise e Visualização de Dados com Python. O projeto explora uma base **simulada** de acidentes de trânsito para identificar padrões por tempo, localidade e gravidade.

## Tecnologias

- Python, Pandas, NumPy, Matplotlib e Seaborn
- Streamlit e Plotly
- SQLite para persistência da base tratada
- Git/GitHub e GitHub Pages

## Estrutura

```text
projeto-g1/
├── app.py
├── requirements.txt
├── README.md
├── index.html
├── dados/acidentes_transito_brasil.csv
├── database/                 # SQLite criado ao executar o dashboard
├── notebooks/analise_acidentes.ipynb
└── imagens/
```

## Como executar

```bash
git clone <URL_DO_REPOSITORIO>
cd projeto-g1
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
streamlit run app.py
```

## Funcionalidades

- Filtros múltiplos e KPIs dinâmicos.
- Análise temporal e comparativa entre regiões e UFs.
- Gráficos interativos, tabela detalhada e exportação do recorte filtrado.
- Persistência da base preparada em SQLite.
- Notebook com todo o percurso da análise.

## Perguntas investigadas

1. Quais regiões e UFs concentram mais acidentes e mortes?
2. Como o volume evolui no tempo?
3. Que tipos de acidente e condições de visibilidade merecem atenção?
4. Onde a mortalidade proporcional é mais elevada?

## Publicação

Depois da publicação, preencha os links abaixo.

- Repositório: `https://github.com/SEU_USUARIO/projeto-g1`
- Página do projeto: `https://SEU_USUARIO.github.io/projeto-g1/`
- Dashboard: `https://SEU_APP.streamlit.app/`

## Limitação

Os dados foram fornecidos como uma simulação educacional. Os resultados não representam estatísticas oficiais de segurança viária.
