import unittest
from binance.client import AsyncClient
from bot_binance.analyzer import AnalyzerFactory, BinanceAnalyzer
from bot_binance.setting_name import *


class TestAnalyzer(unittest.TestCase):
    def test_factory_get_analyzer(self):
        expected_interval = AsyncClient.KLINE_INTERVAL_1MINUTE
        expected_symbol = "BTCUSDT"

        settings = {INTERVAL: expected_interval, SYMBOL: expected_symbol}

        analyser = AnalyzerFactory.get_analyser(AnalyzerFactory.TYPE_BINANCE, **settings)

        self.assertIsInstance(analyser,
                              BinanceAnalyzer,
                              "AnalyzerFactory creates {result} instance "
                              "instead of {expected}".format(result=analyser.__class__.__name__,
                                                             expected=BinanceAnalyzer.__name__))

        result_symbol = analyser.get_symbol()
        self.assertEqual(result_symbol,
                         expected_symbol,
                         "AnalyzerFactory create an analyser "
                         "with {result} instead of {expected}".format(result=result_symbol, expected=expected_symbol))

        result_interval = analyser.get_kline_interval()
        self.assertEqual(result_interval, expected_interval,
                         "AnalyzerFactory create an analyser "
                         "with {result} instead of {expected}".format(result=result_interval,
                                                                      expected=expected_interval))


if __name__ == '__main__':
    unittest.main()
