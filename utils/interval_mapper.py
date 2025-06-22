def get_interval_mapping() -> dict:
    """
    CCXT 및 Binance에서 사용하는 interval 문자열로 변환
    분 단위를 key로 사용.
    """
    return {
        1: '1m', 3: '3m', 5: '5m', 15: '15m', 30: '30m',
        60: '1h', 120: '2h', 240: '4h', 360: '6h',
        720: '12h', 1440: '1d', 4320: '3d',
        10080: '1w', 43200: '1M'
    }

def to_ccxt_interval(minutes: int) -> str:
    """
    CCXT용 문자열 포맷으로 변환 (1m, 5m, 1h 등)
    """
    mapping = get_interval_mapping()
    if minutes not in mapping:
        raise ValueError(f"Unsupported interval: {minutes}")
    return mapping[minutes]

def to_pandas_freq(minutes: int) -> str:
    """
    pandas.resample()에서 사용할 T기반 주기 문자열로 변환
    """
    if not isinstance(minutes, int) or minutes <= 0:
        raise ValueError(f"Invalid interval for pandas: {minutes}")
    return f"{minutes}T"
