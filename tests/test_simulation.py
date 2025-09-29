import unittest
import csv
import tomllib

from blackjack.helper.simulation import calculate_expected_value
import blackjack as bss


class CalculateExpectedValue(unittest.TestCase):
    def test_calculate_expected_value_within_range(self):
        """
        Making sure the calculated expected values is within the minimum and maximum
        possible values.
        """

        # loading a test dictionary from test_data.csv
        # NOTE: test_data is not necessarily accurate, it is just used for the testing of inputs and expected outputs
        with open('test_data.csv') as csv_file:
            reader = csv.reader(csv_file)
            test_dictionary = dict(reader)
        
        # after importing from the test_data.csv, the dictionary is storing the key as a large string, so we need to convert it back to a tuple
        for k,v in test_dictionary.items():
            # eval() converts the string-tuple back into a proper tuple
            # NOTE: by calling global_data_dictionary directly, it shouldn't maintain it's value for the other tests
            bss.global_data_dictionary[eval(k)] = float(v)
        
        # loading setting.toml
        with open("test_settings.toml", "rb") as f:
            test_settings = tomllib.load(f)

        #output is dictionary where the key is (17, "hard", 5, "stand"), and the value is the expected value (float)
        output = calculate_expected_value(sim_case=(17, "hard", 5, "stand"), toml_settings=test_settings)

        # because because the calculated expected value takes the game.value / number of sims
        # the max the expected value could be is 25.00; that is if the player wins every match while betting 25.00
        # 25000.00 / 1000.00 = 25.00
        # vice versa for minimum value
        self.assertGreater(output[(17, "hard", 5, "stand")], -25.00)
        self.assertLess(output[(17, "hard", 5, "stand")], 25.00)


if __name__ == '__main__':
    unittest.main()
