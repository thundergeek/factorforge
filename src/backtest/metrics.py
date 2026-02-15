import numpy as np
import pandas as pd


def information_coefficient(factor: pd.Series, fwd_returns: pd.Series) -> float:
    df = pd.concat([factor, fwd_returns], axis=1, join="inner").dropna()
    if df.empty:
        return np.nan
    return df.rank().corr(method="spearman").iloc[0, 1]


def annualized_return(daily_returns: pd.Series, periods_per_year: int = 252) -> float:
    r = (1 + daily_returns).prod()
    n = len(daily_returns)
    if n == 0:
        return np.nan
    return r ** (periods_per_year / n) - 1


def max_drawdown(daily_returns: pd.Series) -> float:
    cumulative = (1 + daily_returns).cumprod()
    peak = cumulative.cummax()
    dd = (cumulative / peak) - 1
    return dd.min()


def sharpe_ratio(daily_returns: pd.Series, risk_free: float = 0.0) -> float:
    excess = daily_returns - risk_free / 252
    if excess.std() == 0:
        return np.nan
    return np.sqrt(252) * excess.mean() / excess.std()


def compute_metrics(
    factor: pd.Series,
    fwd_returns: pd.Series,
    portfolio_returns: pd.Series,
) -> dict:
    ic = information_coefficient(factor, fwd_returns)
    arr = annualized_return(portfolio_returns)
    mdd = max_drawdown(portfolio_returns)
    sharpe = sharpe_ratio(portfolio_returns)
    return {"ic": ic, "arr": arr, "mdd": mdd, "sharpe": sharpe}
