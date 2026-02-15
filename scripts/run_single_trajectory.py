import argparse

from src.config import settings
from src.data import load_price_history
from src.factors import evaluate_dsl_factor
from src.backtest import backtest_long_short_factor, compute_forward_returns, compute_metrics


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dsl", type=str, default="rolling_mean(close, 10) - rolling_mean(close, 60)")
    args = parser.parse_args()

    symbols = [s.strip() for s in settings.universe_symbols.split(",") if s.strip()]
    prices = load_price_history(symbols)
    factor = evaluate_dsl_factor(args.dsl, prices)
    fwd_ret = compute_forward_returns(prices, horizon=1)
    ls_ret = backtest_long_short_factor(factor, fwd_ret)
    m = compute_metrics(factor, fwd_ret, ls_ret)
    print(f"DSL: {args.dsl}")
    print(f"Metrics: {m}")


if __name__ == "__main__":
    main()
