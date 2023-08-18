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


if __name__ == '__main__':
    unittest.main()
