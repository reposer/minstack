from datetime import timedelta
from typing import List

import ccxt
import pandas as pd

from domain.interfaces.price_batch_fetcher_interface import PriceBatchFetcher
from domain.models.asset_price_record_model import AssetPriceRecordModel
from utils.interval_mapper import to_ccxt_interval
from utils.logger import get_logger


class CCXTPriceFetcher(PriceBatchFetcher):
    def __init__(self):
        self.spot = ccxt.binance()
        self.perp = ccxt.binanceusdm()

    def fetch_ohlcv(
        self,
        symbol: str,
        from_date: str,
        to_date: str,
        interval: int,
        venue: str = "perp"
    ) -> List[AssetPriceRecordModel]:

        exchange = self.perp if venue == "perp" else self.spot
        market_symbol = symbol.replace("_PERP", "") if symbol.endswith("_PERP") else symbol
        tf = to_ccxt_interval(interval)

        if not from_date or not to_date:
            raise ValueError("from_date and to_date are required for batch fetching")

        from_utc = int((pd.to_datetime(from_date) - timedelta(hours=9)).timestamp() * 1000)
        to_utc = int((pd.to_datetime(to_date) - timedelta(hours=9)).timestamp() * 1000)

        all_data = []
        since = from_utc

        while since < to_utc:
            ohlcv = exchange.fetch_ohlcv(market_symbol, tf, since=since, limit=1000)
            if not ohlcv:
                break
            all_data.extend(ohlcv)
            since = ohlcv[-1][0] + 60_000  # 1m 간격

        df = pd.DataFrame(all_data, columns=["timestamp", "open", "high", "low", "close", "volume"])
        df["trade_date"] = pd.to_datetime(df["timestamp"], unit="ms") + timedelta(hours=9)
        df["asset_id"] = symbol
        df["open_interest"] = None

        df = df[[
            "trade_date", "asset_id", "open", "high", "low", "close", "volume", "open_interest"
        ]]
        df = df[(df["trade_date"] >= from_date) & (df["trade_date"] <= to_date)]

        records = [
            AssetPriceRecordModel(
                trade_date=row["trade_date"],
                asset_id=row["asset_id"],
                open=row["open"],
                high=row["high"],
                low=row["low"],
                close=row["close"],
                volume=row["volume"],
                open_interest=row["open_interest"],
            )
            for _, row in df.iterrows()
        ]
        l = get_logger(self)
        l.info(f"Successfully read price records from CCXT.")
        return records

