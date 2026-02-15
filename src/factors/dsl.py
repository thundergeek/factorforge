from typing import Dict
import pandas as pd
import numpy as np

from src.factors.ops import ALLOWED_FUNCS


def evaluate_dsl_factor(dsl_expr: str, prices: pd.DataFrame) -> pd.Series:
    allowed_names = {"open", "high", "low", "close", "volume"} | set(ALLOWED_FUNCS.keys())
    tokens = {t.strip("(), ") for t in dsl_expr.replace("+", " ").replace("-", " ")
              .replace("*", " ").replace("/", " ").split()}
    unknown = {t for t in tokens if t.isidentifier() and t not in allowed_names}
    if unknown:
        raise ValueError(f"Unknown identifiers: {unknown}")

    out_list = []
    for sym, sub in prices.groupby(level="symbol"):
        # Reset index to get simple integer index (avoids datetime buffer issue)
        sub_reset = sub.droplevel("symbol")
        
        local_env: Dict[str, object] = {}
        for col in ["open", "high", "low", "close", "volume"]:
            if col in sub_reset.columns:
                # Keep as Series but with simple integer index
                local_env[col] = sub_reset[col].reset_index(drop=True)
        local_env.update(ALLOWED_FUNCS)
        local_env["np"] = np
        
        result = eval(dsl_expr, {"__builtins__": {}}, local_env)
        # Convert result back to Series with original date index
        if isinstance(result, pd.Series):
            result = result.values
        s = pd.Series(result, index=sub_reset.index, name=sym)
        out_list.append(s)

    res = pd.concat(out_list, axis=0)
    res.index = pd.MultiIndex.from_arrays(
        [res.index, [name for s in out_list for name in [s.name] * len(s)]],
        names=["date", "symbol"]
    )
    return res.sort_index()
