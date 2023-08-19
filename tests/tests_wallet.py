import unittest
from unittest.mock import AsyncMock, patch
from binance import AsyncClient
from bot_binance.wallet import BinanceWallet,ACC_ASSET,ACC_ASSET_LOCK,ACC_BALANCES,ACC_ASSET_FREE


class MyTestCase(unittest.IsolatedAsyncioTestCase):

    client: AsyncMock = AsyncMock()

    async def test_BinanceWallet_get_asset_qty(self):
        btc_asset = 'BTC'
        btc_qty = 1000
        btc_qty_locked = 100
        eth_asset = 'ETH'
        eth_qty = 500
        eth_qty_locked = 0

        account_info_from_binance = {ACC_BALANCES: [{ACC_ASSET: btc_asset,
                                                     ACC_ASSET_FREE: btc_qty,
                                                     ACC_ASSET_LOCK: btc_qty_locked},
                                                    {ACC_ASSET: eth_asset,
                                                     ACC_ASSET_FREE: eth_qty,
                                                     ACC_ASSET_LOCK: eth_qty_locked}]}
        mock_client = AsyncMock()
        mock_instance_client = mock_client.return_value
        mock_instance_client.get_account.return_value = account_info_from_binance

        wallet = BinanceWallet(mock_instance_client)
        btc_qty_from_wallet = await wallet.get_asset_qty(btc_asset)
        expected_btc_qty = btc_qty

        self.assertEqual(expected_btc_qty, btc_qty_from_wallet,
                         "Expected {expected} BTC instead of {result}".format(expected=expected_btc_qty,
                                                                              result=btc_qty_from_wallet))

        btc_qty_from_wallet = await wallet.get_asset_qty(btc_asset, True)
        expected_btc_qty = btc_qty - btc_qty_locked

        self.assertEqual(expected_btc_qty, btc_qty_from_wallet,
                         "Expected {expected} BTC instead of {result}".format(expected=expected_btc_qty,
                                                                              result=btc_qty_from_wallet))

        eth_qty_from_wallet = await wallet.get_asset_qty(eth_asset)
        expected_eth_qty = eth_qty
        self.assertEqual(expected_eth_qty, eth_qty_from_wallet,
                         "Expected {expected} ETH instead of {result}".format(expected=expected_eth_qty,
                                                                              result=eth_qty_from_wallet))

        eth_qty_from_wallet = await wallet.get_asset_qty(eth_asset, True)
        expected_eth_qty = eth_qty - eth_qty_locked
        self.assertEqual(expected_eth_qty, eth_qty_from_wallet,
                         "Expected {expected} ETH instead of {result}".format(expected=expected_eth_qty,
                                                                              result=eth_qty_from_wallet))


if __name__ == '__main__':
    unittest.main()
