from typing import Protocol

import pandas as pd


class PriceBatchFetcher(Protocol):
    def fetch_ohlcv(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        interval: int,
        venue: str = "perp"
    ) -> pd.DataFrame:
        ...
