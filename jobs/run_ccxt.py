import ccxt
import time

# spot = ccxt.binance()
perp = ccxt.binanceusdm()

since = int(time.time() * 1000) - 60 * 1000 * 1000
ohlcv = perp.fetch_ohlcv('XRPBNB', '1m', since=since, limit=1000)

print(ohlcv[:5])