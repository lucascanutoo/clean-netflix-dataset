# Clean Netflix Dataset

Projeto de limpeza e preparacao do dataset `netflix_titles.csv`, com foco em tratar valores ausentes, corrigir inconsistencias de duracao, converter colunas de data e gerar arquivos prontos para analise.

## Objetivo

O projeto recebe o arquivo original em `data/netflix_titles.csv` e gera uma versao limpa em CSV e Pickle, alem de relatorios auxiliares sobre os tratamentos aplicados.

Principais etapas:

- Analise de valores ausentes por coluna.
- Preenchimento de campos textuais ausentes com `Unknown`.
- Correcao de duracoes que estavam registradas indevidamente na coluna `rating`.
- Conversao de `date_added` para uma nova coluna datetime.
- Separacao da coluna `duration` em valor numerico e unidade padronizada.
- Exportacao do dataset limpo e dos relatorios de qualidade.

## Dataset

O dataset original possui:

- 8.807 registros.
- 12 colunas originais.
- Conteudos classificados como `Movie` ou `TV Show`.

Depois da limpeza, o dataset passa a ter 15 colunas, com as novas colunas:

- `date_added_datetime`: versao convertida de `date_added` para data.
- `duration_value`: valor numerico da duracao.
- `duration_unit`: unidade padronizada da duracao, como `minutes` ou `seasons`.

## Saidas Geradas

### Dataset limpo

- `outputs/netflix_titles_clean.csv`: arquivo CSV limpo, indicado para uso em analises e visualizacoes.
- `outputs/netflix_titles_clean.pkl`: versao serializada em Pickle para reutilizacao direta com pandas.

### Relatorios

- `outputs/missing_values_report.csv`: mostra os valores ausentes antes e depois da limpeza e o tratamento aplicado em cada coluna.
- `outputs/mixed_type_columns_report.csv`: documenta colunas com tipos mistos e como foram normalizadas.
- `outputs/date_columns_report.csv`: registra a conversao de colunas de data, incluindo intervalo minimo e maximo encontrado.

## Tratamentos Aplicados

### Valores ausentes

As colunas `director`, `cast`, `country`, `date_added`, `rating` e `duration` recebem `Unknown` quando possuem valores ausentes.

### Correcao de `rating`

Algumas linhas possuem valores de duracao, como `74 min` ou `1 Season`, dentro da coluna `rating`. O script identifica esses casos, move o valor para `duration` quando necessario e limpa o campo incorreto em `rating`.

### Conversao de datas

A coluna `date_added` e mantida em formato textual para preservar o valor original. Uma nova coluna, `date_added_datetime`, e criada com `pd.to_datetime`.

Datas ausentes ou invalidas permanecem como `NaT` na coluna convertida.

### Normalizacao de duracao

A coluna `duration` combina numero e unidade no mesmo texto. Por isso, o projeto cria:

- `duration_value`: numero inteiro da duracao.
- `duration_unit`: unidade textual padronizada.

Exemplos:

```text
90 min    -> duration_value = 90, duration_unit = minutes
2 Seasons -> duration_value = 2, duration_unit = seasons
```

## Notebook

O arquivo `notebook.ipynb` contem uma versao exploratoria do processo, com analise das colunas de data, tratamento de ausentes, validacao de conversoes e exportacao dos resultados.