import unittest
from bot_binance.indicator import sma


class MyTestCase(unittest.TestCase):
    def test_sma(self):
        values = [x for x in range(20)]
        window_size = 10

        result = sma(values, window_size)

        expected_sma_values = [None] * (window_size-1)
        expected_sma_values += [4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5]

        print(values)
        print(result)
        print(expected_sma_values)
        self.assertEqual(len(expected_sma_values), len(result))
        self.assertListEqual(expected_sma_values, result)


if __name__ == '__main__':
    unittest.main()
