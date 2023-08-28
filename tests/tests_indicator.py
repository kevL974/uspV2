import unittest
from bot_binance.indicator import sma, rsi


class MyTestCase(unittest.TestCase):
    def test_sma(self):
        closing_prices = [x for x in range(20)]
        period = 10

        result = sma(closing_prices, period)

        expected_sma_values = [None] * period
        expected_sma_values += [4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5]

        print(expected_sma_values)
        print(result)
        self.assertEqual(len(expected_sma_values),
                         len(result),
                         "Size of SMA results should be {expected} "
                         "instead of {result}".format(expected=len(expected_sma_values), result=len(result)))

        self.assertListEqual(expected_sma_values, result, "SMA results are wrong !")

    def test_rsi(self):
        closing_prices = [12, 11, 12, 14, 18, 12, 15, 13, 16, 12, 11, 13, 15, 14, 16, 18, 22, 19, 24, 17, 19]
        period = 14

        expected_rsi = [None, None, None, None, None, None, None, None, None, None, None, None, None, None,
                        55.88, 60.0, 63.16, 56.41, 57.50, 56.10, 55.00, 57.89]

        rsi_values = rsi(closing_prices, period)
        print(expected_rsi)
        print(rsi_values)
        self.assertEqual(len(expected_rsi),
                         len(rsi_values),
                         "Size of RSI results should be {expected} "
                         "instead of {result}".format(expected=len(expected_rsi), result=len(rsi_values)))

        self.assertListEqual(expected_rsi, rsi_values, "RSI results are wrong !")


if __name__ == '__main__':
    unittest.main()
