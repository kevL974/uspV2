import asyncio
import argparse
from typing import List
from binance import AsyncClient
from bot_binance.utils import *
from bot_binance.wallet import BinanceWallet
from bot_binance.analyzer import Analyzer, AnalyzerFactory
from bot_binance.broker import Broker
from bot_binance.strategy import TradingStrategy, Sma200Rsi10Strategy
from bot_binance.indicator import IndicatorFactory
from bot_binance.setting_name import *
from bot_binance.binance_constants import HistKlinesIndex
from bot_binance.observer import EventType


def create_analyzer(strategy: TradingStrategy) -> Analyzer:
    analyzer_settings = strategy.get_analyzer_settings()
    analyzer = None
    try:
        analyzer = AnalyzerFactory.get_analyser(AnalyzerFactory.TYPE_BINANCE, **analyzer_settings)
    except ValueError as error:
        print(error)

    return analyzer


async def create_required_strategy_indicators(strategy: TradingStrategy, analyzer: Analyzer) -> List:
    required_indicator_plans = strategy.get_required_indicators()
    indicators = []
    for indicator_plan in required_indicator_plans:
        try:
            type, settings = indicator_plan
            indicator = IndicatorFactory.get_indicator(type, **settings)
            hist_klines = await analyzer.get_historical_data(settings[WINDOW])
            hist_klines_cp = get_historical_close_price(hist_klines)
            hist_klines_ct = get_historical_close_time(hist_klines)
            indicator.initialisation(hist_klines_cp, hist_klines_ct)
            indicators.append(indicator)
        except ValueError as error:
            print(error)
    return indicators


async def main(conf_api_key: str, conf_api_secret: str, testnet: bool):
    client = await AsyncClient.create(api_key=conf_api_key, api_secret=conf_api_secret, testnet=testnet)
    wallet = BinanceWallet(client)
    strategy = Sma200Rsi10Strategy()
    broker = Broker(wallet)

    analyzer = create_analyzer(strategy)
    analyzer.set_client(client)
    indicators = await create_required_strategy_indicators(strategy, analyzer)

    for indicator in indicators:
        analyzer.add_observer(EventType.DATA, indicator)
        indicator.add_observer(EventType.DATA, strategy)

    await analyzer.analyze()

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
