from typing import Dict
from bot_binance.wallet import Wallet
from bot_binance.observer import ObserverInterface


class Broker(ObserverInterface):
    """
    This class do trades with a given wallet and a given trading strategy
    """

    def update(self, data: Dict) -> None:
        print(type(data))
        print(data)

    def __init__(self, wallet: Wallet):
        self.wallet = wallet

    async def start_trading(self):
        pass


