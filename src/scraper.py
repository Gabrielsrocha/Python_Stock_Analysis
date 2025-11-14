"""Módulo responsável pela coleta de dados do Fundamentus."""

import logging
from typing import Optional

import pandas as pd
import requests

from .config import FUNDAMENTUS_URL, REQUEST_HEADERS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FundamentusScraperError(Exception):
    """Exceção customizada para erros no scraper."""
    pass


class FundamentusScraper:
    """Scraper para coletar dados fundamentalistas de ações."""

    def __init__(self, url: str = FUNDAMENTUS_URL,
                 headers: dict = REQUEST_HEADERS):
        """
        Inicializa o scraper.

        Args:
            url: URL do site Fundamentus
            headers: Headers HTTP para a requisição
        """
        self.url = url
        self.headers = headers

    def fetch_data(self) -> pd.DataFrame:
        """
        Busca dados do site Fundamentus.

        Returns:
            DataFrame com os dados fundamentalistas

        Raises:
            FundamentusScraperError: Se houver erro na requisição
        """
        try:
            logger.info("Iniciando requisição ao Fundamentus...")
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()

            logger.info("Requisição bem-sucedida. Processando dados...")
            df = pd.read_html(
                response.text,
                decimal=',',
                thousands='.'
            )[0]

            logger.info(f"Dados coletados: {len(df)} empresas encontradas")
            return df

        except requests.RequestException as e:
            error_msg = f"Erro ao fazer requisição: {str(e)}"
            logger.error(error_msg)
            raise FundamentusScraperError(error_msg) from e

        except (ValueError, IndexError) as e:
            error_msg = f"Erro ao processar HTML: {str(e)}"
            logger.error(error_msg)
            raise FundamentusScraperError(error_msg) from e

    def save_to_csv(self, df: pd.DataFrame, filepath: str) -> None:
        """
        Salva DataFrame em arquivo CSV.

        Args:
            df: DataFrame a ser salvo
            filepath: Caminho do arquivo
        """
        try:
            df.to_csv(filepath, index=False)
            logger.info(f"Dados salvos em: {filepath}")
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {str(e)}")
            raise