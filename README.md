# Radar de Segurança Viária no Brasil

**Disciplina:** Linguagens de programação

**Professor:** Alexandre Neves Louzada

**Aluno:** Pedro Rigo de Oliveira

Projeto da Avaliação G1 de Análise e Visualização de Dados com Python. O projeto explora uma base **simulada** de acidentes de trânsito para identificar padrões por tempo, localidade e gravidade.

## Tecnologias

- Python, Pandas, NumPy, Matplotlib e Seaborn
- Streamlit e Plotly
- SQLAlchemy e SQLite para persistência da base tratada
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

## Notebook no Google Colab

O arquivo [analise_acidentes.ipynb](notebooks/analise_acidentes.ipynb) é compatível com o Google Colab e contém as dez etapas exigidas na avaliação. Para abri-lo, use o botão abaixo ou faça upload do arquivo `.ipynb` em [Google Colab](https://colab.research.google.com/).

[![Abrir no Google Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/pdroliv1/projeto_linguagem_programacao/blob/main/notebooks/analise_acidentes.ipynb)

## Perguntas investigadas

1. Quais regiões e UFs concentram mais acidentes e mortes?
2. Como o volume evolui no tempo?
3. Que tipos de acidente e condições de visibilidade merecem atenção?
4. Onde a mortalidade proporcional é mais elevada?

## Publicação

Depois da publicação, preencha os links abaixo.

- Repositório: `https://github.com/pdroliv1/projeto_linguagem_programacao`
- Página do projeto: `https://pdroliv1.github.io/projeto_linguagem_programacao/`
- Dashboard: `https://projetolinguagemprogramacao-afqffujnhobakhtgkc425j.streamlit.app/`

## Limitação

Os dados foram fornecidos como uma simulação educacional. Os resultados não representam estatísticas oficiais de segurança viária.
