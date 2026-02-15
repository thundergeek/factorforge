import pandas as pd
import numpy as np


def rolling_mean(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window, min_periods=1).mean()


def rolling_std(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window, min_periods=1).std()


def pct_change(series: pd.Series, periods: int = 1) -> pd.Series:
    return series.pct_change(periods)


def rolling_rank(series: pd.Series, window: int) -> pd.Series:
    """Rank within rolling window (0-1 normalized)"""
    return series.rolling(window, min_periods=1).apply(
        lambda x: pd.Series(x).rank(pct=True).iloc[-1], raw=False
    )


def zscore(series: pd.Series, window: int) -> pd.Series:
    """Z-score normalization over rolling window"""
    mean = series.rolling(window, min_periods=1).mean()
    std = series.rolling(window, min_periods=1).std()
    return (series - mean) / (std + 1e-8)


def ts_rank(series: pd.Series, window: int) -> pd.Series:
    """Time-series rank (percentile of current value vs past window)"""
    return series.rolling(window, min_periods=1).apply(
        lambda x: (x[-1] > x).sum() / len(x) if len(x) > 0 else 0.5, 
        raw=True
    )


def ts_delay(series: pd.Series, periods: int) -> pd.Series:
    """Lag the series by N periods"""
    return series.shift(periods)


def ts_delta(series: pd.Series, periods: int) -> pd.Series:
    """Difference from N periods ago"""
    return series - series.shift(periods)


def ts_min(series: pd.Series, window: int) -> pd.Series:
    """Rolling minimum"""
    return series.rolling(window, min_periods=1).min()


def ts_max(series: pd.Series, window: int) -> pd.Series:
    """Rolling maximum"""
    return series.rolling(window, min_periods=1).max()


def correlation(series1: pd.Series, series2: pd.Series, window: int) -> pd.Series:
    """Rolling correlation between two series"""
    return series1.rolling(window, min_periods=1).corr(series2)


ALLOWED_FUNCS = {
    "rolling_mean": rolling_mean,
    "rolling_std": rolling_std,
    "pct_change": pct_change,
    "rolling_rank": rolling_rank,
    "zscore": zscore,
    "ts_rank": ts_rank,
    "ts_delay": ts_delay,
    "ts_delta": ts_delta,
    "ts_min": ts_min,
    "ts_max": ts_max,
}
