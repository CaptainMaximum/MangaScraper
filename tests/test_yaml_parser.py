import unittest

from yaml_parser import *

class TestSequenceFunctions(unittest.TestCase):
    # 
    def test_get_yaml_dict__valid(self):
        expected = {'url': 'http://something.com', 'name': 'Gintama', 'volumes': {'V1': [1, 2]}}
        observed = get_yaml_dict("tests/test_files/test.yaml")
        self.assertEqual( expected, observed)

    def test_get_yaml_dict__invalid(self):
        expected = None
        observed = get_yaml_dict("nonexistent.yaml")
        self.assertEqual(expected, observed)

    def test_find_missing_params__complete(self):
        expected = []
        observed = find_missing_params({'name': "foo", 'url': "http://www.example.com", 'volumes': "vols"})
        self.assertEqual(expected, observed)

    def test_find_missing_params__incomplete(self):
        expected = ["name"]
        observed = find_missing_params({'url': "http://www.example.com", 'volumes': "vols"})
        self.assertEqual(expected,observed)

if __name__ == "__main__":
    unittest.main()