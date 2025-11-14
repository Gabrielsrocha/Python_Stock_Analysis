"""Script principal para executar a análise fundamentalista."""
import argparse
import sys
from pathlib import Path

from src.scraper import FundamentusScraper, FundamentusScraperError
from src.processor import DataProcessor
from src.ranker import FactorRanker



def main(mode: str = 'global', top_n: int = 20, save_csv: bool = False,
         output_dir: str = 'data') -> int:
    """
    Executa o pipeline completo de análise.

    Args:
        top_n: Número de ações no ranking
        save_csv: Se deve salvar os dados em CSV
        output_dir: Diretório para salvar os arquivos

    Returns:
        0 se sucesso, 1 se erro
    """
    try:
        # Coleta de dados
        print("\n🔍 Coletando dados do Fundamentus...")
        scraper = FundamentusScraper()
        df_raw = scraper.fetch_data()

        if save_csv:
            Path(output_dir).mkdir(parents=True, exist_ok=True)
            scraper.save_to_csv(
                df_raw,
                f"{output_dir}/fundamentus_raw.csv"
            )

        # Processamento
        print("🔧 Processando e filtrando dados...")
        processor = DataProcessor()

        if not processor.validate_data(df_raw):
            print("❌ Erro: Dados inválidos ou incompletos")
            return 1

        df_clean = processor.clean_data(df_raw)
        df_filtered = processor.apply_filters(df_clean)

        if len(df_filtered) == 0:
            print("⚠️  Aviso: Nenhuma ação passou pelos filtros")
            return 1

        print(f"✅ {len(df_filtered)} empresas passaram nos filtros")

        # Ranking global
        print(f"\n📊 Calculando ranking global (Top {top_n})...")
        ranker = FactorRanker()
        df_ranking = ranker.calculate_ranks(df_filtered)
        df_final = ranker.calculate_final_score(df_ranking)

        # Exibe relatório
        report = ranker.generate_report(df_final, top_n)
        print(report)

        if save_csv:
            df_final.to_csv(
                f"{output_dir}/ranking_global.csv",
                index=False
            )
            print(f"\n💾 Ranking salvo em: {output_dir}/ranking_global.csv")


        print(report)


        return 0

    except FundamentusScraperError as e:
        print(f"❌ Erro ao coletar dados: {e}")
        return 1
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Análise fundamentalista de ações brasileiras",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  
  Ranking global top 20:
    python main.py
  
  Ranking global top 50:
    python main.py -n 50
  
        """
    )


    parser.add_argument(
        '-n', '--top',
        type=int,
        default=20,
        help='Número de ações no ranking . Padrão: 20'
    )

    parser.add_argument(
        '-s', '--save',
        action='store_true',
        help='Salvar dados em CSV'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default='data',
        help='Diretório de saída. Padrão: data/'
    )

    args = parser.parse_args()

    sys.exit(main(
        top_n=args.top,
        save_csv=args.save,
        output_dir=args.output
    ))