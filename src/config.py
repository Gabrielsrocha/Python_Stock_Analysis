"""Configurações do projeto de análise fundamentalista."""

# URL base para scraping
FUNDAMENTUS_URL = 'http://www.fundamentus.com.br/resultado.php'

# Headers para requisição
REQUEST_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/84.0.4147.89 Safari/537.36"
    )
}

# Colunas para tratamento percentual
PERCENTAGE_COLUMNS = [
    'Div.Yield',
    'Mrg. Líq.',
    'P/L',
    'ROE',
    'Cresc. Rec.5a',
    'EV/EBIT'
]

# Colunas para ranking
RANKING_COLUMNS = [
    'Papel',
    'Div.Yield',
    'Mrg. Líq.',
    'P/L',
    'ROE',
    'Cresc. Rec.5a',
    'EV/EBIT'
]

# Pesos para o cálculo do ranking
RANKING_WEIGHTS = {
    'Div.Yield rank': 1.0,
    'Mrg. Líq. rank': 1.0,
    'P/L rank': 1.4,
    'ROE rank': 1.4,
    'Cresc. Rec.5a rank': 1.2,
    'EV/EBIT rank': 1.0
}

# Critérios de filtro
FILTER_CRITERIA = {
    'min_liquidity': 100000,
    'max_debt_equity': 1.0,
    'min_profit_margin': 0.1,
    'max_pe_ratio': 25,
    'min_revenue_growth': 0.1
}