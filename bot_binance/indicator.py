from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
from collections import deque
from bot_binance.observer import ObserverInterface, ObservableInterface, EventType
from bot_binance.indicator_setting_name import *


class Indicator(ObserverInterface, ObservableInterface):

    def __init__(self, name: str):
        self._strategy_list_observers: List = {}
        self._name: str = name

    def add_observer(self, event_type: str, observer: ObserverInterface) -> None:
        if event_type not in self._strategy_list_observers:
            self._strategy_list_observers[event_type] = []

        event_type_observers = self._strategy_list_observers[event_type]
        event_type_observers.append(observer)

    def remove_observer(self, observer: ObserverInterface) -> None:
        for event_type, observers in self._strategy_list_observers:
            if observer in observers:
                observers.remove(observer)

    def notify(self, event_type: str, data) -> None:
        if event_type in self._strategy_list_observers:
            event_type_observers = self._strategy_list_observers[event_type]
            for observer_i in event_type_observers:
                observer_i.update(data)

    def get_full_name(self) -> str:
        return Indicator.NAME + self.get_parameter()

    def get_hist_klines_settings(self) -> Dict:
        """
        Returns settings required in order to get historical candlelines from exchange.
        @return: Dict object
        """
        return self._hist_klines_settings

    @abstractmethod
    def initialisation(self, hist_klines: List) -> None:
        """
        Do required initialisation to compute indicator value.
        @return: None
        """
        pass

    @abstractmethod
    def get_parameters(self) -> Dict:
        pass

    @abstractmethod
    def value(self) -> Tuple:
        pass


class SmaIndicator(Indicator):
    """
    An indicator that implements Simple Moving Average.

    Requirements :
        -Historical candlelines to compute SMA
        -Define window size

    Both requirements should be defined in 'settings' constructor parameters.
    """

    def __init__(self, name: str = "sma", window: int = 10):
        super().__init__(name)
        self.__window_size: int = window
        self.__hist_klines_cp = deque(maxlen=self.__window_size)
        self.__hist_klines_ct = deque(maxlen=self.__window_size)

    def initialisation(self, hist_klines_cp: List, hist_klines_ct: List) -> None:
        for cp in hist_klines_cp:
            self.__hist_klines_cp.append(cp)

        for ct in hist_klines_ct:
            self.__hist_klines_ct.append(ct)

    def update(self, data: Dict) -> None:
        close_price = data['k']['c'];print(data)
        close_time = data['k']['T']
        self.__hist_klines_cp.popleft()
        self.__hist_klines_cp.append(float(close_price))
        self.__hist_klines_ct.popleft()
        self.__hist_klines_ct.append(int(close_time))
        data = {NAME: self._name, VALUE: self.value()}
        self.notify(EventType.DATA, data)

    def get_parameters(self) -> Dict:
        return {WINDOW: self.__window_size}

    def value(self) -> Tuple:
        return self.__hist_klines_ct[-1], sma(self.__hist_klines_cp, self.__window_size)


class RsiIndicator(Indicator):

    def __init__(self, name: str = "rsi", window: int = 10):
        super().__init__(name)
        self.__window_size: int = window

    def value(self) -> float:
        pass

    def get_parameter(self) -> str:
        pass

    def update(self, data: Dict) -> None:
        pass


class IndicatorFactory:
    """
    A factory that produices indicator.
    """

    TYPE_SMA: int = 1
    TYPE_RSI: int = 2

    @staticmethod
    def get_indicator(type: int, **kwargs) -> Indicator:
        """
        Factory method that returns the appropriate indicator according to the given type in parameters.
        @param type: indicator type.
        @param kwargs: parameters according to the indicator type.
        @return: an Indicator object.
        """
        indicator = None
        if IndicatorFactory.TYPE_SMA == type:
            indicator = SmaIndicator(**kwargs)
        elif IndicatorFactory.TYPE_RSI == type:
            indicator = RsiIndicator(**kwargs)
        else:
            raise ValueError("Indicator type {} unknowned".format(str(type)))
        return indicator


def sma(values: List, window_size: int) -> float:
    """
    Calculate simple moving average values from a list of value according to window size given in parameter
    @param values: a list of element
    @param window_size: a number that defines the size of window
    @return: List of simple moving average
    """
    nb_values = len(values)
    moving_average = [None] * nb_values
    index_values = 0
    iem_values = 1
    while iem_values <= nb_values:

        if iem_values - window_size >= 0:
            average_i = sum(values) / window_size
            moving_average[index_values] = average_i

        iem_values += 1
        index_values += 1

    return moving_average[-1]
