import asyncio
import argparse
from binance import AsyncClient, BinanceSocketManager
from bot_binance.utils import *
from bot_binance.wallet import BinanceWallet


async def main(conf_api_key: str, conf_api_secret: str, testnet: bool):
    client = await AsyncClient.create(api_key=conf_api_key, api_secret=conf_api_secret, testnet=testnet)
    info = await client.get_account()

    wallet = BinanceWallet(client)
    print('BTC qty = {}'.format(str(await wallet.get_asset_qty('BTC'))))
    print(info)
    bm = BinanceSocketManager(client)
    # start any sockets here, i.e a trade socket
    ts = bm.kline_socket('BNBBTC',)
    # then start receiving messages
    async with ts as tscm:
        while True:
            res = await tscm.recv()
            print(res)

    await client.close_connection()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Make some trades with Binance')
    parser.add_argument('-c', '--config', help='path to bot configuration file.', type=str, required=True)
    parser.add_argument('--testnet', help='use binance testnet platform', action='store_true')
    parser.add_argument('--debug', help='activate debug mode', action='store_true')
    args = parser.parse_args()

    configuration_path = args.config
    testnet_mode = args.testnet
    debug_mode = args.debug

    config = load_api_keys_from_yaml_file(configuration_path)

    if testnet_mode:
        api_key = config[CONFIG_YAML_API_DEMO_SECTION][CONFIG_YAML_API_KEY_VAR]
        api_secret = config[CONFIG_YAML_API_DEMO_SECTION][CONFIG_YAML_API_SECRET_VAR]
    else:
        api_key = config[CONFIG_YAML_API_DEMO_SECTION][CONFIG_YAML_API_KEY_VAR]
        api_secret = config[CONFIG_YAML_API_DEMO_SECTION][CONFIG_YAML_API_SECRET_VAR]

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(api_key, api_secret, testnet_mode))
