"""Testes para o módulo scraper."""

import unittest
from unittest.mock import Mock, patch, MagicMock
import pandas as pd
import requests

from src.scraper import FundamentusScraper, FundamentusScraperError


class TestFundamentusScraper(unittest.TestCase):
    """Testes para a classe FundamentusScraper."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.scraper = FundamentusScraper()
        self.sample_html = """
        <table>
            <tr><th>Papel</th><th>P/L</th></tr>
            <tr><td>PETR4</td><td>5,5</td></tr>
            <tr><td>VALE3</td><td>3,2</td></tr>
        </table>
        """

    @patch('src.scraper.requests.get')
    @patch('src.scraper.pd.read_html')
    def test_fetch_data_success(self, mock_read_html, mock_get):
        """Testa coleta de dados bem-sucedida."""
        # Configura mocks
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = self.sample_html
        mock_get.return_value = mock_response

        mock_df = pd.DataFrame({
            'Papel': ['PETR4', 'VALE3'],
            'P/L': [5.5, 3.2]
        })
        mock_read_html.return_value = [mock_df]

        # Executa
        result = self.scraper.fetch_data()

        # Valida
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        mock_get.assert_called_once()

    @patch('src.scraper.requests.get')
    def test_fetch_data_request_error(self, mock_get):
        """Testa erro de requisição."""
        mock_get.side_effect = requests.RequestException("Erro de rede")

        with self.assertRaises(FundamentusScraperError):
            self.scraper.fetch_data()

    @patch('src.scraper.requests.get')
    @patch('src.scraper.pd.read_html')
    def test_fetch_data_parse_error(self, mock_read_html, mock_get):
        """Testa erro ao fazer parse do HTML."""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "HTML inválido"
        mock_get.return_value = mock_response

        mock_read_html.side_effect = ValueError("Não encontrou tabela")

        with self.assertRaises(FundamentusScraperError):
            self.scraper.fetch_data()

    @patch('builtins.open', create=True)
    def test_save_to_csv(self, mock_open):
        """Testa salvamento em CSV."""
        df = pd.DataFrame({'Papel': ['PETR4'], 'P/L': [5.5]})
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        # Não deve lançar exceção
        self.scraper.save_to_csv(df, 'test.csv')


if __name__ == '__main__':
    unittest.main()