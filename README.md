# 📊 Stock Fundamental Analysis

Automated system for analyzing and ranking Brazilian stocks (B3) based on fundamental indicators using Factor Investing methodology.

> ⚠️ **Disclaimer**: Educational purposes only. Not financial advice.

## Features

- Web scraping from Fundamentus
- Quality filters based on fundamental indicators
- Multi-factor weighted ranking system
- CSV export and reporting

## Installation

```bash
git clone https://github.com/seu-usuario/stock-fundamental-analysis.git
cd stock-fundamental-analysis
pip install -r requirements.txt
```

## Usage

```bash
# Global ranking (top 20)
python main.py

# Global ranking (top 50)
python main.py -n 50

# Custom output directory
python main.py -m sector -n 20 -s -o results
```

## Indicators

| Indicator | Weight | Description |
|-----------|--------|-------------|
| Dividend Yield | 1.0 | Dividend return |
| Net Margin | 1.0 | Profitability |
| P/E Ratio | 1.3 | Valuation |
| ROE | 1.4 | Return on equity |
| Revenue Growth (5y) | 1.2 | Historical growth |
| EV/EBIT | 1.0 | Valuation multiple |

## Filter Criteria

- Liquidity (2m) > R$ 100,000
- Debt/Equity < 1.0
- P/E: 0 < P/E ≤ 25
- Net Margin > 10%
- Revenue Growth (5y) > 10%

## Project Structure

```
├── src/
│   ├── scraper.py      # Data collection
│   ├── processor.py    # Data processing
│   ├── ranker.py       # Ranking system
│   └── config.py       # Settings
├── tests/              # Unit tests
├── main.py             # Main script
└── requirements.txt
```

## Testing

```bash
pytest tests/ -v
```

## Technologies

- Python 3.8+
- Pandas, Requests
- Pytest


---

# 📊 Análise Fundamentalista de Ações

Sistema automatizado para análise e ranking de ações brasileiras (B3) baseado em indicadores fundamentalistas utilizando Factor Investing.

> ⚠️ **Aviso**: Apenas para fins educacionais. Não constitui recomendação de investimento.

## Funcionalidades

- Web scraping do Fundamentus
- Filtros de qualidade baseados em indicadores fundamentalistas
- Sistema de ranking ponderado por múltiplos fatores
- Exportação para CSV e relatórios

## Instalação

```bash
git clone https://github.com/seu-usuario/stock-fundamental-analysis.git
cd stock-fundamental-analysis
pip install -r requirements.txt
```

## Uso

```bash
# Uso básico
python main.py

# Top 30 ações
python main.py -n 30

# Salvar resultados em CSV
python main.py -s -o data
```

## Indicadores

| Indicador | Peso | Descrição |
|-----------|------|-----------|
| Dividend Yield | 1.0 | Rendimento de dividendos |
| Margem Líquida | 1.0 | Lucratividade |
| P/L | 1.4 | Valuation |
| ROE | 1.4 | Retorno sobre patrimônio |
| Cresc. Receita (5a) | 1.2 | Crescimento histórico |
| EV/EBIT | 1.0 | Múltiplo de valuation |

## Critérios de Filtro

- Liquidez (2m) > R$ 100.000
- Dívida/Patrimônio < 1,0
- P/L: 0 < P/L ≤ 25
- Margem Líquida > 10%
- Crescimento Receita (5a) > 10%

## Estrutura do Projeto

```
├── src/
│   ├── scraper.py      # Coleta de dados
│   ├── processor.py    # Processamento
│   ├── ranker.py       # Sistema de ranking
│   └── config.py       # Configurações
├── tests/              # Testes unitários
├── main.py             # Script principal
└── requirements.txt
```

## Testes

```bash
pytest tests/ -v
```

## Tecnologias

- Python 3.8+
- Pandas, Requests
- Pytest

