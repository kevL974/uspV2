import configparser
from typing import List
from bot_binance.binance_constants import HistKlinesIndex

CONFIG_YAML_API_DEMO_SECTION = "api_binance_demo"
CONFIG_YAML_API_SECTION = "api_binance_demo"
CONFIG_YAML_API_SECTION = "api_binance"
CONFIG_YAML_API_KEY_VAR = "api_key"
CONFIG_YAML_API_SECRET_VAR = "api_secret"


def get_historical_close_price(hist_klines: List[List]) -> List[float]:
    """
    Returns list of close price values from historical candlelines.
    @param hist_klines: Historical Klines from Binance
    @return: list of close price values
    """
    assert hist_klines is not None
    return list(map(float, [kline[HistKlinesIndex.CLOSE] for kline in hist_klines]))


def get_historical_close_time(hist_klines: List[List]) -> List[float]:
    """
    Returns list of close price values from historical candlelines.
    @param hist_klines: Historical Klines from Binance
    @return: list of close price values
    """
    assert hist_klines is not None
    return list(map(float, [kline[HistKlinesIndex.CLOSE_TIME] for kline in hist_klines]))


def convert_timeunit_abrv_to_full(time_unit: str) -> str:
    """
    Function that converts time unit abbreviation to full name.
    @param time_unit: time unit abbreviation to convert
    @return: time unit in full name
    """
    if time_unit == "m":
        return "minutes"
    elif time_unit == "h":
        return "hours"
    elif time_unit == "d":
        return "days"
    elif time_unit == "w":
        return "weeks"
    elif time_unit == "M":
        return "months"
    else:
        ValueError("'{}' abbreviation unknowned.".format(time_unit))

def load_api_keys_from_yaml_file(path: str) -> configparser.ConfigParser:
    """
    Load cryptocurrency exchange api keys from yaml file.
    @param path: YAML file where api keys are stored
    @return: ConfigParser object
    """
    config_bot = configparser.ConfigParser()
    config_bot.read(path)
    return config_bot
