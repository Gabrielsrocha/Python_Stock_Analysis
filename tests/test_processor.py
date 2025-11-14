"""Testes para o módulo processor."""

import unittest
import pandas as pd
import numpy as np

from src.processor import DataProcessor


class TestDataProcessor(unittest.TestCase):
    """Testes para a classe DataProcessor."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.processor = DataProcessor()
        self.sample_df = pd.DataFrame({
            'Papel': ['PETR4', 'VALE3', 'ITUB4'],
            'Div.Yield': ['5,5%', '6,2%', '8,1%'],
            'P/L': ['10,5', '8,3', '12,0'],
            'ROE': ['15,5%', '20,0%', '18,2%'],
            'Mrg. Líq.': ['12,0%', '15,5%', '20,1%'],
            'Cresc. Rec.5a': ['10,5%', '12,0%', '15,0%'],
            'EV/EBIT': ['8,5', '7,2', '9,1'],
            'Liq.2meses': [150000, 200000, 180000],
            'Dív.Brut/ Patrim.': [0.5, 0.3, 0.8]
        })

    def test_convert_percentage(self):
        """Testa conversão de percentuais."""
        series = pd.Series(['5,5%', '10,2%', '15,0%'])
        result = self.processor._convert_percentage(series)

        self.assertAlmostEqual(result[0], 0.055, places=3)
        self.assertAlmostEqual(result[1], 0.102, places=3)
        self.assertAlmostEqual(result[2], 0.150, places=3)

    def test_clean_data(self):
        """Testa limpeza dos dados."""
        result = self.processor.clean_data(self.sample_df)

        # Verifica se percentuais foram convertidos
        self.assertIsInstance(result['Div.Yield'][0], float)
        self.assertTrue(result['Div.Yield'][0] < 1)

    def test_apply_filters_liquidity(self):
        """Testa filtro de liquidez."""
        df_clean = self.processor.clean_data(self.sample_df)
        result = self.processor.apply_filters(
            df_clean,
            {'min_liquidity': 180000, 'max_debt_equity': 1.0,
             'min_profit_margin': 0.0, 'max_pe_ratio': 100,
             'min_revenue_growth': 0.0}
        )

        # Deve ter apenas 2 empresas (>= 180000)
        self.assertEqual(len(result), 2)

    def test_apply_filters_debt(self):
        """Testa filtro de endividamento."""
        df_clean = self.processor.clean_data(self.sample_df)
        result = self.processor.apply_filters(
            df_clean,
            {'min_liquidity': 0, 'max_debt_equity': 0.6,
             'min_profit_margin': 0.0, 'max_pe_ratio': 100,
             'min_revenue_growth': 0.0}
        )

        # Deve ter apenas 2 empresas (< 0.6)
        self.assertEqual(len(result), 2)

    def test_validate_data_success(self):
        """Testa validação de dados válidos."""
        df_clean = self.processor.clean_data(self.sample_df)
        result = self.processor.validate_data(df_clean)
        self.assertTrue(result)

    def test_validate_data_missing_columns(self):
        """Testa validação com colunas faltando."""
        df_incomplete = self.sample_df[['Papel', 'P/L']].copy()
        result = self.processor.validate_data(df_incomplete)
        self.assertFalse(result)

    def test_empty_dataframe_filter(self):
        """Testa filtro em DataFrame vazio."""
        empty_df = pd.DataFrame()
        result = self.processor.apply_filters(empty_df)
        self.assertEqual(len(result), 0)


if __name__ == '__main__':
    unittest.main()