import unittest
import os
from bot_binance.utils import *

TEST_YAML_FILE = "test_yaml_file.ini"
API_KEY_VALUE = "api_key_value"
API_SECRET_VALUE = "api_secret_value"


class TestsUtils(unittest.TestCase):

    def setUp(self) -> None:
        with open(TEST_YAML_FILE, 'w') as yaml_file:
            yaml_file.write(
                "[{yaml_api_section}]\n"
                "{yaml_api_key_var} = {api_key_value}\n"
                "{yaml_api_secret_var} = {api_secret_value}\n".format(yaml_api_section=CONFIG_YAML_API_DEMO_SECTION,
                                                                      yaml_api_key_var=CONFIG_YAML_API_KEY_VAR,
                                                                      yaml_api_secret_var=CONFIG_YAML_API_SECRET_VAR,
                                                                      api_key_value=API_KEY_VALUE,
                                                                      api_secret_value=API_SECRET_VALUE
                                                                      )
            )

    def tearDown(self) -> None:
        os.remove(TEST_YAML_FILE)

    def test_load_api_keys_from_yaml_file(self) -> None:
        api_keys_loaded = load_api_keys_from_yaml_file(TEST_YAML_FILE)

        expected_api_key_val = API_KEY_VALUE
        api_key_val = api_keys_loaded[CONFIG_YAML_API_DEMO_SECTION][CONFIG_YAML_API_KEY_VAR]

        expected_api_secret_val = API_SECRET_VALUE
        api_secret_val = api_keys_loaded[CONFIG_YAML_API_DEMO_SECTION][CONFIG_YAML_API_SECRET_VAR]

        self.assertEqual(expected_api_key_val,
                         api_key_val,
                         "Wrong api key value : {expected} instead of {result}".format(expected=expected_api_key_val,
                                                                                       result=api_key_val))

        self.assertEqual(expected_api_secret_val,
                         api_secret_val,
                         "Wrong api key value : {expected} instead of {result}".format(expected=expected_api_secret_val,
                                                                                       result=api_secret_val))

    def test_get_historical_close_price(self):
        expected_hist_cp = [26046.0, 26057.74]
        hist_klines = [[1692941220000, '26048.02000000', '26048.02000000', '26040.76000000', str(expected_hist_cp[0]),
                        '2.66325800', 1692941279999, '69362.45675895', 74, '0.57613000', '15004.54066359', '0'],
                       [1692941280000, '26046.00000000', '26058.57000000', '26045.99000000', str(expected_hist_cp[1]),
                        '3.69770200', 1692941339999, '96331.26698120', 90, '3.69086400', '96153.11545508', '0']]
        result_hist_cp = get_historical_close_price(hist_klines)
        self.assertListEqual(expected_hist_cp,
                             result_hist_cp,
                             "get_historical_close_price doesn't return close prices values :"
                             " {result} instead of {expected}".format(result=result_hist_cp, expected=expected_hist_cp))

    def test_get_historical_close_time(self):
        expected_hist_ct = [1692941279999, 1692941339999]
        hist_klines = [
            [1692941220000, '26048.02000000', '26048.02000000', '26040.76000000', '26046.00000000',
             '2.66325800', expected_hist_ct[0], '69362.45675895', 74, '0.57613000', '15004.54066359', '0'],
            [1692941280000, '26046.00000000', '26058.57000000', '26045.99000000', '26057.74000000',
             '3.69770200', expected_hist_ct[1], '96331.26698120', 90, '3.69086400', '96153.11545508', '0']]
        result_hist_ct = get_historical_close_time(hist_klines)
        self.assertListEqual(expected_hist_ct,
                             result_hist_ct,
                             "get_historical_close_time doesn't return close time values :"
                             " {result} instead of {expected}".format(result=result_hist_ct,
                                                                      expected=expected_hist_ct))


if __name__ == '__main__':
    unittest.main()
