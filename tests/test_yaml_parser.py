import unittest

from yaml_parser import *

class TestSequenceFunctions(unittest.TestCase):

    # Tests the yaml parser to make sure it converts it correctly to a dictionary 
    # object
    def test_dict_from_yaml_file__valid(self):
        expected = {
            'url': 'http://something.com', 
            'name': 'Gintama', 
            'volumes': 
            {
                'V1': 
                {
                    'other_chapters': [1.5], 
                    'start_chapter': 0,
                    'end_chapter': 3
                }
            }
        }
        observed = dict_from_yaml_file("tests/test_files/test.yaml")
        self.assertEqual( expected, observed)

    # Tests dict_from_yaml_file with a file that doesn't exist to make sure the function
    # returns None
    def test_dict_from_yaml_file__nonexist(self):
        expected = None
        observed = dict_from_yaml_file("nonexistent.yaml")
        self.assertEqual(expected, observed)

    # Tests dict_from_yaml_file with an improperly formatted yaml file to make sure the 
    # function returns -1
    def test_dict_from_yaml_file__invalid(self):
        expected = -1
        observed = dict_from_yaml_file("tests/test_files/bad.yaml")

    # Tests find_missing_params with a dictionary that is not missing any required
    # parameters to ensure that the function returns an empty list
    def test_find_missing_params__complete(self):
        expected = []
        observed = find_missing_params({'name': "foo", 'url': "http://www.example.com", 'volumes': "vols"})
        self.assertEqual(expected, observed)

    # Tests find_missing_params with an incomplete dictionary to ensure that the 
    # function returns a list of what parameters are missing
    def test_find_missing_params__incomplete(self):
        expected = ["name"]
        observed = find_missing_params({'url': "http://www.example.com", 'volumes': "vols"})
        self.assertEqual(expected,observed)

    # Tests safe_get_value to obtain a value for a key that exists in the dict
    def test_safe_get_value__valid(self):
        expected = "bar"
        _input = {"foo": "bar", "baz": "bat", "tick": "tock"}
        observed = safe_get_value(_input, "foo")
        self.assertEqual(expected, observed)

    # Tests safe_get_value with a key that is not in the dict to ensure that the
    # function returns the 'fail' value
    def test_safe_get_value__invalid(self):
        expected = None
        _input = {"foo": "bar", "baz": "bat", "tick": "tock"}
        observed = safe_get_value(_input, "not in")
        self.assertEqual(expected, observed)

    # Tests get_volume_chapters with input that is properly formatted (i.e if a
    # start chapter exists, then an end chapter must also exist) to ensure that
    # the function returns a string->list mapped dict
    def test_get_volume_chapters__valid(self):
        expected = {'V1': [1,2,3], 'V2': [4,5,6,5.5], 'V3': [7,8,9]}
        _input = {
            'V1': {
                'start_chapter': 1,
                'end_chapter': 3
            },
            'V2': {
                'start_chapter': 4,
                'end_chapter': 6,
                'other_chapters': [5.5]
            },
            'V3': {
                'other_chapters': [7, 8, 9]
            }
        }
        observed = get_volume_chapters(_input)
        self.assertEqual(expected, observed)

    # Tests get_volume_chapters with input that is improperly formatted (i.e if
    # a start chapter exists and an end chapter does not) to ensure that the
    # function returns an 'error dict' that specifies the first volume that has
    # improper formatting
    def test_get_volume_chapters__invalid(self):
        expected = {'error': 'V2'}
        _input = {
            'V1': {
                'start_chapter': 1,
                'end_chapter': 3
            },
            'V2': {
                'start_chapter': 1,
                'other_chapters': [2,3,4]
            }
        }
        observed = get_volume_chapters(_input)
        self.assertEqual(expected, observed)

    # Tests get_volume_chapters with no input to ensure that it returns an
    # empty dict
    def test_get_volume_chapters__empty(self):
        expected = {}
        _input = {}
        observed = get_volume_chapters(_input)
        self.assertEqual(expected, observed)

    # Tests stringify_volume_list to ensure that it returns a properly formatted
    # string representing a bash variable assignment
    def test_stringify_volume_list(self):
        expected = "VOLS='$V1 $V2 $V3 $V4'"
        observed = stringify_volume_list(['V1', 'V2', 'V3', 'V4'])
        self.assertEqual(expected, observed)

    # Tests stringify_volume_list with input containing spaces to ensure that
    # the function removes the spaces from the names
    def test_stringify_volume_list_spaces(self):
        expected = "VOLS='$Vol1 $Vol2 $Vol3'"
        observed = stringify_volume_list(['Vol 1', 'Vol 2', 'Vol 3'])
        self.assertEqual(expected, observed)

    # Tests chapters_to_bash_assignments to ensure that the function returns
    # a list of strings representing bash variable assignments
    def test_chapters_to_bash_assignments(self):
        expected = ["V1='*V1* 1 2 3 4'", "V2='*V2* 5 6 7 8'"]
        _input = {
            'V1': [1, 2, 3, 4],
            'V2': [5, 6, 7, 8]
        }
        observed = chapters_to_bash_assignments(_input)
        self.assertEqual(expected, observed)

    # Tests chapters_to_bash_assignments with volume names containing spaces
    # to ensure that the spaces are removed from the variable name, but not in
    # the actual assigned value (the name in stars) because the name in stars
    # is what the file name will eventually be
    def test_chapters_to_bash_assignmetns_spaces(self):
        expected = ["Vol1='*Vol 1* 1 2 3'", "Vol2='*Vol 2* 4 5 6'"]
        _input = {
            'Vol 1': [1, 2, 3],
            'Vol 2': [4, 5, 6]
        }
        observed = chapters_to_bash_assignments(_input)
        self.assertEqual(expected, observed)

if __name__ == "__main__":
    unittest.main()