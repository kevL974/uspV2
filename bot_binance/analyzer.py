from abc import abstractmethod
from binance import AsyncClient, BinanceSocketManager
from typing import Dict, List
from bot_binance.observer import EventType, ObserverInterface, ObservableInterface
from bot_binance.indicator_setting_name import *
from bot_binance.utils import convert_timeunit_abrv_to_full


class Analyzer(ObservableInterface):

    def __init__(self, symbol: str = "BTCUSDT", interval: str = "1m"):
        self._symbol: str = symbol
        self._interval: str = interval
        self._observers: Dict = {}

    def get_symbol(self) -> str:
        return self._symbol

    def set_symbol(self, symbol: str) -> None:
        self._symbol = symbol

    def get_kline_interval(self) -> str:
        return self._interval

    def set_kline_interval(self, interval: str) -> None:
        if not self.is_valid_kline_interval(interval):
            raise ValueError(f"Invalid interval : {interval}".format(interval=interval))
        self._interval = interval

    @abstractmethod
    def is_valid_kline_interval(self, interval: str) -> bool:
        """
        Check if candleline interval given in parameter is valid.
        @param interval: candleline interval in string format
        @return: True if interval is valid, else False
        """
        pass

    @abstractmethod
    def set_client(self, client) -> None:
        pass

    @abstractmethod
    def _initialize_websocket(self) -> None:
        """
        Initialize client websocket.
        @return: None
        """
        pass

    @abstractmethod
    async def _start_websocket(self) -> None:
        """
        Launch websocket stream.
        @return: None
        """
        pass

    @abstractmethod
    async def get_historical_data(self, period: int) -> List:
        pass

    async def analyze(self):
        self._initialize_websocket()
        await self._start_websocket()


class BinanceAnalyzer(Analyzer):

    PERIOD_SUFFIX_UTC = "ago UTC"
    LIST_KLINE_INTERVAL = [AsyncClient.KLINE_INTERVAL_1MINUTE,
                           AsyncClient.KLINE_INTERVAL_3MINUTE,
                           AsyncClient.KLINE_INTERVAL_5MINUTE,
                           AsyncClient.KLINE_INTERVAL_15MINUTE,
                           AsyncClient.KLINE_INTERVAL_30MINUTE,
                           AsyncClient.KLINE_INTERVAL_1HOUR,
                           AsyncClient.KLINE_INTERVAL_2HOUR,
                           AsyncClient.KLINE_INTERVAL_6HOUR,
                           AsyncClient.KLINE_INTERVAL_8HOUR,
                           AsyncClient.KLINE_INTERVAL_12HOUR,
                           AsyncClient.KLINE_INTERVAL_1DAY,
                           AsyncClient.KLINE_INTERVAL_3DAY,
                           AsyncClient.KLINE_INTERVAL_1WEEK,
                           AsyncClient.KLINE_INTERVAL_1MONTH]

    def __init__(self, symbol: str = "BTCUSDT", interval: str = "1m"):
        super().__init__(symbol, interval)
        self.__client = None

    def set_client(self, client) -> None:
        self.__client: AsyncClient = client

    def is_valid_kline_interval(self, interval: str) -> bool:
        return interval in BinanceAnalyzer.LIST_KLINE_INTERVAL

    def _initialize_websocket(self) -> None:
        self.__socket_manager = BinanceSocketManager(self.__client)

    async def _start_websocket(self,) -> None:
        ts = self.__socket_manager.kline_socket(self._symbol, self._interval)
        async with ts as tscm:
            while True:
                res = await tscm.recv()
                self.notify(EventType.DATA, res)

    def add_observer(self, event_type: str, observer: ObserverInterface) -> None:
        if event_type not in self._observers:
            self._observers[event_type] = []

        event_type_observers = self._observers[event_type]
        event_type_observers.append(observer)

    def remove_observer(self, observer: ObserverInterface) -> None:
        for event_type, observers in self._observers:
            if observer in observers:
                observers.remove(observer)

    def notify(self, event_type: str, data) -> None:
        if event_type in self._observers:
            event_type_observers = self._observers[event_type]
            for observer_i in event_type_observers:
                observer_i.update(data)

    async def get_historical_data(self, period: int) -> List:
        qty = int(self._interval[:-1])*period
        time_unit = convert_timeunit_abrv_to_full(self._interval[-1])
        return await self.__client.get_historical_klines(self._symbol,
                                                        self._interval,
                                                        "{qty}{time_unit} {suffix}".format(qty=str(qty),
                                                                                           time_unit=time_unit,
                                                                                           suffix=BinanceAnalyzer.
                                                                                           PERIOD_SUFFIX_UTC))


class AnalyzerFactory:
    """
        A factory that produces analyzers.
    """
    TYPE_BINANCE = 1

    @staticmethod
    def get_analyser(type: int, **settings) -> Analyzer:
        """
        Factory method that returns the appropriate analyzer according to the given type in parameters.
        @param type: analyzer type.
        @param settings: parameters according to the analyzer type.
        @return: an Analyzer object.
        """
        interval = settings.get(INTERVAL, None)
        symbol = settings.get(SYMBOL, None)
        if interval is None:
            raise ValueError("Candleline interval setting is missing !")

        if symbol is None:
            raise ValueError("Candlelin symbol setting is missing !")

        analyzer = None
        if AnalyzerFactory.TYPE_BINANCE == type:
            analyzer = BinanceAnalyzer(symbol, interval)
        else:
            raise ValueError("Analyzer type {} unknowned".format(str(type)))

        return analyzer
