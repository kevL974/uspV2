from abc import ABC, abstractmethod
from binance import AsyncClient, BinanceSocketManager
from typing import Dict, List
from bot_binance.binance_constants import HistKlinesIndex
from bot_binance.indicator import sma


class Analyser(ABC):

    @abstractmethod
    async def _get_historical_data(self, symbol: str, interval: str, period: str) -> List:
        ...

    @abstractmethod
    async def get_indicators(self, symbol: str) -> Dict:
        ...


class BinanceAnalyser(Analyser):

    INTERVAL: str = AsyncClient.KLINE_INTERVAL_15MINUTE
    PERIOD: str = "3000 minutes ago UTC"

    def __init__(self, client: AsyncClient):
        assert client is not None
        self._client = client
        self._socket_manager = BinanceSocketManager(client)

    async def _get_historical_data(self, symbol: str, interval: str, period: str) -> List:
        return await self._client.get_historical_klines(symbol, interval, period)

    async def get_indicators(self, symbol: str) -> Dict:
        hist_klines = await self._get_historical_data(symbol, BinanceAnalyser.INTERVAL, BinanceAnalyser.PERIOD)
        close_price_values = [float(kline[HistKlinesIndex.CLOSE]) for kline in hist_klines]
        sma_values_20 = sma(close_price_values, 20)
        sma_values_10 = sma(close_price_values, 10)
        print(sma_values_20)
        print(sma_values_10)
