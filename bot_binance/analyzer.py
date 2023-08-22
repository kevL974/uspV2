from abc import ABC, abstractmethod
from binance import AsyncClient, BinanceSocketManager
from typing import Dict, List
from bot_binance.binance_constants import HistKlinesIndex
from bot_binance.indicator import sma
from bot_binance.observer import EventType, ObserverInterface, ObservableInterface


class Analyzer(ABC):

    @abstractmethod
    def _initialize_websocket(self) -> None:
        """
        Initialize websocket client.
        @return: None
        """
        ...

    @abstractmethod
    async def _start_websocket(self, symbol: str) -> None:
        """
        Process to receive messages from websocket for the given symbol.
        @param symbol: name of cryptocurrency
        @return: None
        """

    @abstractmethod
    async def _get_historical_data(self, symbol: str, interval: str, period: str) -> List:
        ...

    @abstractmethod
    async def get_indicators(self, symbol: str) -> Dict:
        ...

    async def analyze(self, symbol: str):
        self._initialize_websocket()
        await self._start_websocket(symbol)


class BinanceAnalyzer(Analyzer, ObservableInterface):

    INTERVAL: str = AsyncClient.KLINE_INTERVAL_15MINUTE
    PERIOD: str = "3000 minutes ago UTC"

    def __init__(self, client: AsyncClient):
        assert client is not None
        self._client: AsyncClient = client
        self._observers: Dict = {}

    def _initialize_websocket(self) -> None:
        self.__socket_manager = BinanceSocketManager(self._client)

    async def _start_websocket(self, symbol: str) -> None:
        ts = self.__socket_manager.kline_socket(symbol)
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                self.notify(EventType.SIGNAL, res)

    def add_observer(self, event_type: EventType, observer: ObserverInterface) -> None:
        if event_type not in self._observers:
            self._observers[event_type] = []

        event_type_observers = self._observers[event_type]
        event_type_observers.append(observer)

    def remove_observer(self, observer: ObserverInterface) -> None:
        for event_type, observers in self._observers:
            if observer in observers:
                observers.remove(observer)

    def notify(self, event_type: EventType, data) -> None:
        if event_type in self._observers:
            event_type_observers = self._observers[event_type]
            for observer_i in event_type_observers:
                observer_i.update(data)

    async def _get_historical_data(self, symbol: str, interval: str, period: str) -> List:
        return await self._client.get_historical_klines(symbol, interval, period)

    async def get_indicators(self, symbol: str) -> None:
        hist_klines = await self._get_historical_data(symbol, BinanceAnalyzer.INTERVAL, BinanceAnalyzer.PERIOD)
        close_price_values = [float(kline[HistKlinesIndex.CLOSE]) for kline in hist_klines]
        sma_values_20 = sma(close_price_values, 20)
        sma_values_10 = sma(close_price_values, 10)
        print(sma_values_20)
        print(sma_values_10)
