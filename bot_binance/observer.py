from abc import ABC, abstractmethod
from typing import Dict


class EventType:

    SIGNAL: str = "SIGNAL"
    DATA: str = "DATA"


class ObserverInterface(ABC):
    """
    This interface provides Observer's methods to implements Observer design pattern.
    """

    @abstractmethod
    def update(self, data: Dict) -> None:
        """
        Update observer object from new data.
        @param data: the notified data
        @return: None
        """
        pass


class ObservableInterface(ABC):
    """
    This interface provides Observable's methods to implements Observer design pattern.
    """
    @abstractmethod
    def add_observer(self, event_type: str, observer: ObserverInterface) -> None:
        """
        Add observer object to a collection for the given event type.
        @param event_type: the type of event that will be notified
        @param observer: an object that needs to be notified from an event.
        @return: None
        """
        pass

    @abstractmethod
    def remove_observer(self, observer: ObserverInterface) -> None:
        """
        Remove observer object to a collection.
        @param observer: an object that needs to be notified from an event.
        @return: None
        """
        pass

    @abstractmethod
    def notify(self, event_type: str, data) -> None:
        """
        Notify an event for all observer objects concerned.
        @param event_type: the type of event that will be notified
        @param data: the notified data
        @return: None
        """
        pass
