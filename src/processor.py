"""Módulo para processamento e limpeza de dados."""

import logging
from typing import List

import pandas as pd
import numpy as np

from .config import PERCENTAGE_COLUMNS, FILTER_CRITERIA

logger = logging.getLogger(__name__)


class DataProcessor:
    """Classe para processar e filtrar dados fundamentalistas."""

    def __init__(self, percentage_cols: List[str] = PERCENTAGE_COLUMNS):
        """
        Inicializa o processador.

        Args:
            percentage_cols: Lista de colunas com valores percentuais
        """
        self.percentage_cols = percentage_cols

    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Limpa e formata os dados do DataFrame.

        Args:
            df: DataFrame com dados brutos

        Returns:
            DataFrame com dados limpos
        """
        df_clean = df.copy()

        for col in self.percentage_cols:
            if col in df_clean.columns:
                df_clean[col] = self._convert_percentage(df_clean[col])

        logger.info("Dados limpos e formatados")
        return df_clean

    @staticmethod
    def _convert_percentage(series: pd.Series) -> pd.Series:
        """
        Converte string percentual para float.

        Args:
            series: Série com valores em formato string

        Returns:
            Série com valores numéricos
        """
        try:
            converted = (
                series
                .astype(str)
                .str.replace('.', '', regex=False)
                .str.replace(',', '.', regex=False)
                .str.rstrip('%')
                .astype(float) / 100
            )
            return converted
        except Exception as e:
            logger.warning(f"Erro ao converter percentual: {str(e)}")
            return series

    def apply_filters(self, df: pd.DataFrame,
                     criteria: dict = FILTER_CRITERIA) -> pd.DataFrame:
        """
        Aplica filtros de qualidade aos dados.

        Args:
            df: DataFrame com dados limpos
            criteria: Dicionário com critérios de filtro

        Returns:
            DataFrame filtrado
        """
        df_filtered = df.copy()
        initial_count = len(df_filtered)

        # Filtro de liquidez
        if 'Liq.2meses' in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered['Liq.2meses'] > criteria['min_liquidity']
            ]

        # Filtro de endividamento
        if 'Dív.Brut/ Patrim.' in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered['Dív.Brut/ Patrim.'] < criteria['max_debt_equity']
            ]

        # Filtro de P/L
        if 'P/L' in df_filtered.columns:
            df_filtered = df_filtered[
                (df_filtered['P/L'] > 0) &
                (df_filtered['P/L'] <= criteria['max_pe_ratio'])
            ]

        # Filtro de margem líquida
        if 'Mrg. Líq.' in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered['Mrg. Líq.'] > criteria['min_profit_margin']
            ]

        # Filtro de crescimento de receita
        if 'Cresc. Rec.5a' in df_filtered.columns:
            df_filtered = df_filtered[
                df_filtered['Cresc. Rec.5a'] > criteria['min_revenue_growth']
            ]

        final_count = len(df_filtered)
        logger.info(
            f"Filtros aplicados: {initial_count} -> {final_count} empresas"
        )

        return df_filtered

    def validate_data(self, df: pd.DataFrame) -> bool:
        """
        Valida se o DataFrame contém as colunas necessárias.

        Args:
            df: DataFrame a ser validado

        Returns:
            True se válido, False caso contrário
        """
        required_cols = ['Papel'] + self.percentage_cols
        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            logger.error(f"Colunas faltando: {missing_cols}")
            return False

        return True