from bot_binance.wallet import Wallet
from bot_binance.strategy import TradingStrategy
from bot_binance.observer import ObserverInterface


class Broker(ObserverInterface):
    """
    This class do trades with a given wallet and a given trading strategy
    """

    def update(self, data) -> None:
        print(type(data))
        print(data)

    def __init__(self, wallet: Wallet, strategy: TradingStrategy):
        self.wallet = wallet
        self.strategy = strategy

    async def start_trading(self):
        pass


