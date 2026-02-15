import pandas as pd
import numpy as np


def compute_forward_returns(prices: pd.DataFrame, horizon: int = 1) -> pd.Series:
    close = prices["close"].unstack("symbol")
    fwd = close.shift(-horizon) / close - 1.0
    fwd = fwd.stack()
    fwd.name = "fwd_ret"
    return fwd


def backtest_long_short_factor(
    factor: pd.Series,
    fwd_returns: pd.Series,
    long_pct: float = 0.1,
    short_pct: float = 0.1,
) -> pd.Series:
    df = pd.concat([factor.rename("factor"), fwd_returns], axis=1, join="inner").dropna()
    daily_pnl = []

    for date, sub in df.groupby(level="date"):
        s = sub.droplevel("date")
        n = len(s)
        if n < 10:
            continue
        k_long = max(1, int(n * long_pct))
        k_short = max(1, int(n * short_pct))

        ranked = s["factor"].rank(method="first")
        longs = ranked.nlargest(k_long).index
        shorts = ranked.nsmallest(k_short).index

        long_ret = s.loc[longs, "fwd_ret"].mean()
        short_ret = s.loc[shorts, "fwd_ret"].mean()
        pnl = 0.5 * long_ret - 0.5 * short_ret
        daily_pnl.append((date, pnl))

    if not daily_pnl:
        return pd.Series(dtype=float)

    dates, rets = zip(*daily_pnl)
    return pd.Series(rets, index=pd.Index(dates, name="date"), name="ls_ret").sort_index()
