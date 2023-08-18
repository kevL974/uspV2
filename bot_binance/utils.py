import configparser

CONFIG_YAML_API_DEMO_SECTION = "api_binance_demo"
CONFIG_YAML_API_SECTION = "api_binance_demo"
CONFIG_YAML_API_SECTION = "api_binance"
CONFIG_YAML_API_KEY_VAR = "api_key"
CONFIG_YAML_API_SECRET_VAR = "api_secret"


def load_api_keys_from_yaml_file(path: str) -> configparser.ConfigParser:
    """
    Load cryptocurrency exchange api keys from yaml file.
    @param path: YAML file where api keys are stored
    @return: ConfigParser object
    """
    config_bot = configparser.ConfigParser()
    config_bot.read(path)
    return config_bot
