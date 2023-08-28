from abc import abstractmethod
from typing import List, Dict, Tuple
from binance import AsyncClient
from bot_binance.observer import ObserverInterface, ObservableInterface, EventType
from bot_binance.setting_name import *
from bot_binance.indicator import IndicatorFactory


class TradingStrategy(ObserverInterface, ObservableInterface):

    @abstractmethod
    def get_required_indicators(self) -> List:
        pass

    @abstractmethod
    def get_analyzer_settings(self) -> Dict:
        pass

    @abstractmethod
    def is_buy_condition(self):
        pass

    @abstractmethod
    def set_indicator_value(self, indicator_name: str, value: Tuple) -> None:
        pass


class Sma200Rsi10Strategy(TradingStrategy):

    def __init__(self):
        super().__init__()
        self.__sma: float = 0.0
        self._sma_t: int = 0
        self.__rsi: float = 0.0
        self.__rsi_t: int = 0
        self._brokers_list = []

    def set_indicator_value(self, indicator_name: str, value: Tuple) -> None:
        if indicator_name == "sma200":
            self.__sma = value[1]
            self._sma_t = value[0]

        elif indicator_name == "rsi10":
            self.__rsi = value[1]
            self.__rsi_t = value[0]

        else:
            raise ValueError("{} indicator is not expected".format(indicator_name))

    def get_required_indicators(self) -> List:
        return [
            (IndicatorFactory.TYPE_SMA,
             {
                 NAME: "sma200",
                 WINDOW: 200
             }
             ),
            (IndicatorFactory.TYPE_RSI,
             {
                 NAME: "rsi10",
                 WINDOW: 10
             }
             ),
        ]

    def get_analyzer_settings(self) -> Dict:
        return {SYMBOL: "BTCUSDT", INTERVAL: AsyncClient.KLINE_INTERVAL_1MINUTE}

    def is_buy_condition(self):
        pass

    def update(self, data: Dict) -> None:
        self.set_indicator_value(data[NAME], data[VALUE])

    def add_observer(self, event_type: str, observer: ObserverInterface) -> None:
        if EventType.SIGNAL == event_type:
            self._brokers_list.append(observer)

    def remove_observer(self, observer: ObserverInterface) -> None:
        if observer in self._brokers_list:
            self._brokers_list.remove(observer)

    def notify(self, event_type: str, data) -> None:
        for broker in self._brokers_list:
            broker.update(data)
