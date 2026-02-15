from pathlib import Path
from typing import List
import pandas as pd
import yfinance as yf

from src.config import settings


def load_price_history(
    symbols: List[str],
    start: str | None = None,
    end: str | None = None,
    cache: bool = True,
) -> pd.DataFrame:
    start = start or settings.start_date
    end = end or settings.end_date

    cache_path = settings.data_dir / "raw_prices.parquet"
    if cache and cache_path.exists():
        return pd.read_parquet(cache_path)

    df = yf.download(
        tickers=symbols,
        start=start,
        end=end,
        auto_adjust=False,
        group_by="ticker",
        progress=False,
    )

    frames = []
    for sym in symbols:
        if sym not in df.columns.levels[0]:
            continue
        sub = df[sym].copy()
        sub.columns = [c.lower() for c in sub.columns]
        sub["symbol"] = sym
        frames.append(sub)

    if not frames:
        raise RuntimeError("No data downloaded")

    out = pd.concat(frames)
    out.index.name = "date"
    out.reset_index(inplace=True)
    out.set_index(["date", "symbol"], inplace=True)
    out.sort_index(inplace=True)

    cache_path.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(cache_path)

    return out
