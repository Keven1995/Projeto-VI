# Projeto de Visualizacao da Informacao

Projeto em Python para consumir dados reais da API do TMDB, tratar o dataset com pandas e gerar tres visualizacoes relacionadas sobre **filmes mais bem avaliados de 2025**.

As visualizacoes escolhidas foram:

- grafico de linha;
- grafico de barras;
- diagrama de cordas.

## Guia rapido para visualizar os graficos

Depois de baixar ou clonar o projeto, entre na pasta do projeto:

```powershell
cd "Projeto VI"
```

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale as dependencias:

```powershell
python -m pip install -e ".[dev]"
```

Crie o arquivo `.env` a partir do modelo:

```powershell
Copy-Item env.example .env
```

Preencha o `.env` com pelo menos uma credencial do TMDB:

```text
TMDB_READ_TOKEN=seu_token_de_leitura
TMDB_API_KEY=sua_api_key
```

Gere os graficos finais:

```powershell
python -m viz_api_project
```

Abra os arquivos gerados:

```powershell
start output\tmdb_2025_avaliacao_linha.png
start output\tmdb_2025_avaliacao_barras.png
start output\tmdb_2025_avaliacao_cordas.png
```

Se a pessoa nao tiver credencial do TMDB, ainda pode testar o funcionamento com dados locais:

```powershell
python -m viz_api_project.cli --config configs\local_sample_dataset.json
```

## Tema do dataset

O dataset é consumido dinamicamente da API do TMDB usando o endpoint `discover/movie`.

Recorte utilizado:

- filmes lancados em 2025;
- ordenacao por maior avaliacao media;
- minimo de 100 votos por filme;

Filtros principais em `configs/tmdb_top_rated_2025.json`:

```json
{
  "primary_release_year": 2025,
  "primary_release_date.gte": "2025-01-01",
  "primary_release_date.lte": "2025-12-31",
  "sort_by": "vote_average.desc",
  "vote_count.gte": 100
}
```

Depois do consumo da API, os dados sao transformados em um dataset limpo com campos como:

- `title`;
- `release_date`;
- `release_year`;
- `release_month`;
- `vote_average`;
- `vote_count`;
- `popularity`;
- `original_language`;
- `primary_genre`;
- `genre_names`.

## Requisitos do trabalho

O projeto atende aos requisitos:

- usa dados reais;
- consome dados de uma API;
- implementa as visualizacoes em Python;
- usa tres tecnicas de visualizacao;
- mantem os graficos relacionados ao mesmo dataset;
- aplica organizacao em camadas e boas praticas de clean code.

## Como instalar

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Como configurar a API do TMDB

Crie um arquivo `.env` na raiz do projeto a partir do modelo:

```powershell
Copy-Item env.example .env
```

Depois preencha pelo menos uma credencial:

```text
TMDB_READ_TOKEN=seu_token_de_leitura
TMDB_API_KEY=sua_api_key
```

O projeto prioriza `TMDB_READ_TOKEN`, usando autenticação via header:

```text
Authorization: Bearer <token>
```

Se o token nao existir, usa `TMDB_API_KEY` como parametro `api_key`.

## Como gerar os graficos finais

```powershell
python -m viz_api_project
```

Os arquivos serao gerados em `output`:

- `output/tmdb_2025_avaliacao_linha.png`;
- `output/tmdb_2025_avaliacao_barras.png`;
- `output/tmdb_2025_avaliacao_cordas.png`.

Para abrir no Windows:

```powershell
start output\tmdb_2025_avaliacao_linha.png
start output\tmdb_2025_avaliacao_barras.png
start output\tmdb_2025_avaliacao_cordas.png
```

## Logica dos graficos

### Grafico de linha

Arquivo: `src/viz_api_project/charts/line.py`

Config atual:

```json
{
  "x": "release_month",
  "y": "vote_average",
  "aggregation": "mean"
}
```

Esse grafico agrupa os filmes por mes de lancamento e calcula a media de `vote_average`. Ele mostra como a avaliacao media dos filmes de 2025 varia ao longo dos meses.

### Grafico de barras

Arquivo: `src/viz_api_project/charts/bar.py`

Config atual:

```json
{
  "x": "title",
  "y": "vote_average",
  "top_n": 15
}
```

Esse grafico apresenta os 15 filmes mais bem avaliados do recorte, usando `vote_average` como valor principal.

### Diagrama de cordas

Arquivo: `src/viz_api_project/charts/chord.py`

Config atual:

```json
{
  "source": "original_language",
  "target": "primary_genre",
  "value": "vote_count",
  "top_n": 20
}
```

Esse grafico relaciona idioma original e genero principal. A espessura das conexoes representa o volume de votos (`vote_count`). Para manter a leitura clara, sao exibidas as 20 conexoes mais relevantes.

## Fluxo de execucao

```text
CLI
 -> Config
 -> VisualizationFacade
 -> Repository
 -> TmdbClient
 -> HttpAdapter
 -> TMDB API
 -> dados brutos
 -> Service Layer
 -> transformacao com pandas
 -> CleanDatasetDTO
 -> VisualizationService
 -> Chart Strategies
 -> PNGs em output/
```

## Arquitetura

O projeto segue os padroes:

- Repository;
- Service Layer;
- Adapter;
- Strategy;
- DTO;
- Facade.

Estrutura principal:

```text
src/viz_api_project/
  adapters/              Adaptadores externos, como HTTP
  api/                   Clientes especificos de APIs
  charts/                Implementacao dos graficos
  data/                  Normalizacao e transformacao de dados
  dtos/                  Objetos de transporte de dados limpos
  facades/               Entrada simples para esconder a composicao interna
  repositories/          Acesso aos dados brutos
  services/              Regras de aplicacao e orquestracao
  strategies/            Estrategias para gerar cada tipo de grafico
  cli.py                 Entrada por linha de comando
  config.py              Leitura das configuracoes
  pipeline.py            Compatibilidade para executar a Facade
```

### Responsabilidades

- `HttpAdapter`: encapsula chamadas HTTP.
- `TmdbClient`: conhece endpoints e autenticacao do TMDB.
- `TmdbMovieRepository`: busca dados brutos de filmes e generos.
- `MovieDatasetService`: cria o dataset limpo.
- `CleanDatasetDTO`: transporta o dataset limpo e seus metadados.
- `VisualizationFacade`: esconde a composicao das camadas internas.
- `VisualizationService`: executa as estrategias de graficos.
- `LineChartStrategy`, `BarChartStrategy`, `ChordChartStrategy`: selecionam a forma de construir cada grafico.

## Como rodar os testes

```powershell
python -m pytest -q
```

## Como rodar com dados locais de exemplo

Tambem existe um dataset local simples para testar o fluxo sem depender da API:

```powershell
python -m viz_api_project.cli --config configs\local_sample_dataset.json
```
