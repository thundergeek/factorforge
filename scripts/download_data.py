import argparse

from src.config import settings
from src.data import load_price_history


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--symbols", type=str, default=settings.universe_symbols)
    args = parser.parse_args()
    symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
    df = load_price_history(symbols, cache=False)
    print(f"✅ Downloaded {len(symbols)} symbols, {len(df)} rows")


if __name__ == "__main__":
    main()
