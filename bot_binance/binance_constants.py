# Dictionnaries english to french
# Quote asset volume-> Devis volumes d'actifs
# Taker buy base asset volume -> Volume d'actifs de base d'achat preneur

class HistKlinesIndex:
    """
    Contains OHLCV index from return of binance client method 'get_historical_klines(**params)'
    """
    OPEN_TIME: int = 0
    OPEN: int = 1
    HIGHT: int = 2
    LOW: int = 3
    CLOSE: int = 4
    VOLUME: int = 5
    CLOSE_TIME: int = 6
    QUOTE_ASSET_VOLUME: int = 7
    NUMBER_TRADES: int = 8
    TB_BASE_ASSET_VOLUME: int = 9
    TB_QUOTE_ASSET_VOLUME: int = 10
    IGNORE: int = 11


