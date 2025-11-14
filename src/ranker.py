"""Módulo para criar ranking de ações baseado em fatores."""

import logging
from typing import List, Dict

import pandas as pd

from .config import RANKING_COLUMNS, RANKING_WEIGHTS

logger = logging.getLogger(__name__)


class FactorRanker:
    """Classe para criar ranking baseado em múltiplos fatores."""

    def __init__(self, columns: List[str] = RANKING_COLUMNS,
                 weights: Dict[str, float] = RANKING_WEIGHTS):
        """
        Inicializa o ranker.

        Args:
            columns: Colunas a serem incluídas no ranking
            weights: Pesos para cada fator
        """
        self.columns = columns
        self.weights = weights

    def calculate_ranks(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula os ranks individuais para cada métrica.

        Args:
            df: DataFrame com dados filtrados

        Returns:
            DataFrame com colunas de rank adicionadas
        """
        ranking_df = df[self.columns].copy()

        # Métricas onde maior é melhor
        ranking_df['Div.Yield rank'] = ranking_df['Div.Yield'].rank(
            method='max'
        )
        ranking_df['Mrg. Líq. rank'] = ranking_df['Mrg. Líq.'].rank(
            method='max'
        )
        ranking_df['ROE rank'] = ranking_df['ROE'].rank(method='max')
        ranking_df['Cresc. Rec.5a rank'] = ranking_df['Cresc. Rec.5a'].rank(
            method='max'
        )

        # Métricas onde menor é melhor
        ranking_df['P/L rank'] = ranking_df['P/L'].rank(
            method='max',
            ascending=False
        )
        ranking_df['EV/EBIT rank'] = ranking_df['EV/EBIT'].rank(
            method='max',
            ascending=False
        )

        logger.info("Ranks calculados para todas as métricas")
        return ranking_df

    def calculate_final_score(self, ranking_df: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula o score final ponderado.

        Args:
            ranking_df: DataFrame com ranks individuais

        Returns:
            DataFrame com score total ordenado
        """
        score_df = ranking_df[[
            'Papel',
            'Div.Yield rank',
            'Mrg. Líq. rank',
            'P/L rank',
            'ROE rank',
            'Cresc. Rec.5a rank',
            'EV/EBIT rank'
        ]].copy()

        # Calcula score total com pesos
        score_df['Score Total'] = sum(
            score_df[rank_col] * weight
            for rank_col, weight in self.weights.items()
        )

        # Ordena por score (maior é melhor)
        score_df = score_df.sort_values(by='Score Total', ascending=False)
        score_df = score_df.reset_index(drop=True)

        logger.info(f"Ranking final calculado para {len(score_df)} empresas")
        return score_df

    def get_top_stocks(self, ranking_df: pd.DataFrame,
                      top_n: int = 20) -> pd.DataFrame:
        """
        Retorna as top N ações do ranking.

        Args:
            ranking_df: DataFrame com ranking completo
            top_n: Número de ações a retornar

        Returns:
            DataFrame com top N ações
        """
        return ranking_df.head(top_n)

    def generate_report(self, ranking_df: pd.DataFrame,
                       top_n: int = 20) -> str:
        """
        Gera relatório formatado do ranking.

        Args:
            ranking_df: DataFrame com ranking
            top_n: Número de ações no relatório

        Returns:
            String com relatório formatado
        """
        top_stocks = self.get_top_stocks(ranking_df, top_n)

        report = [
            "\n" + "="*60,
            "ANÁLISE FUNDAMENTALISTA - FACTOR INVESTING",
            "="*60,
            "\nAVISO LEGAL:",
            "Este ranking é apenas para fins educacionais e informativos.",
            "Não constitui recomendação de compra ou venda de ativos.",
            "Sempre faça sua própria análise antes de investir.",
            "\n" + "-"*60,
            f"\nTOP {top_n} AÇÕES RANQUEADAS:",
            "-"*60,
            "\n"
        ]

        for idx, row in top_stocks.iterrows():
            report.append(
                f"{idx + 1}. {row['Papel']:8s} - "
                f"Score: {row['Score Total']:.2f}"
            )

        return "\n".join(report)