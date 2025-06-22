from dataclasses import dataclass
from datetime import datetime


@dataclass
class AssetPriceRecordModel:
    trade_date: datetime
    asset_id: str
    open: float
    high: float
    low: float
    close: float
    volume: float
    open_interest: float