import asyncio
import json
from binance import AsyncClient
from typing import Dict, Optional, List, Tuple, Union


class Wallet:
    """
    This class stores binance account information.
    """

    def __init__(self):
        self.assets: Dict = None

    def get_qty(self, asset: str, with_lock: bool = False) -> float:
        """
        Function that returns qunatity of asset given on parameters.
        @param asset: target asset
        @param with_lock: if True, it returns asset quantity minus quantity locked by previous orders
        else it returns total quantity

        @return: asset quantity
        """
        assert self.assets is not None
        assets_list = self.assets['balances']
        for asset_i in assets_list:
            if asset_i['asset'] == asset:
                if with_lock:
                    return asset_i['free'] - asset_i['locked']
                else:
                    return asset_i['free']

    async def update(self, client: AsyncClient) -> None:
        """
        Function that reachs information about user account, like assets status,
        on Binance server and loads in wallet attributs
        client

        :param client: a Binance AsyncClient object instanced with API keys
        :return: None
        """
        assert client is not None
        self.assets = await client.get_account()
        await client.close_connection()


if __name__ == '__main__':
    api_secret = 'qT7djlAEzP2dB9Q5ShfKWFJkbh9wj3j7UsK9HCzchTwHzKoEq3BcAk6Cs2xdW857'
    api_key = 'sPaQAsAnER9fGXQQqfXS47ruUFWD5BNQpLq4l7olKKrkc2zCOcyEsWwrQg25Lf9r'
    client = AsyncClient(api_key=api_key, api_secret=api_secret, testnet=True)

    wallet = Wallet()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(wallet.update(client=client))

    print('BTCUSDT qty = {}'.format(str(wallet.get_qty('BTC'))))
