# from secret_schema_validation import __version__
import os
import unittest
import warnings
from secret_schema_validation import generator

SCHEMA = {
    '$schema':
    'http://json-schema.org/schema#',
    'type':
    'object',
    'properties': {
        'username': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        },
        'engine': {
            'type': 'string'
        },
        'host': {
            'type': 'string'
        },
        'port': {
            'type': 'string'
        },
        'dbname': {
            'type': 'string'
        },
        'queueName': {
            'type': 'string'
        },
        'topicName': {
            'type': 'string'
        }
    },
    'required': [
        'dbname', 'engine', 'host', 'password', 'port', 'queueName',
        'topicName', 'username'
    ]
}

FILE_PATH = f"{os.getcwd()}/tesxxt_schema.json"


class TestGenerateSchema(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore",
                                category=ResourceWarning,
                                message="unclosed.*<ssl.SSLSocket.*>")

    def test_generate_schema(self):
        self.assertEqual(generator.generate_schema("sc3-dev-db"), SCHEMA)


class TestWriteSchema(unittest.TestCase):

    def setUp(self):
        warnings.filterwarnings("ignore",
                                category=ResourceWarning,
                                message="unclosed.*<ssl.SSLSocket.*>")

    def tearDown(self):
        if os.path.exists(FILE_PATH):
            os.remove(FILE_PATH)
        else:
            print("Can not delete the file as it doesn't exists")

    def test_write_schema(self):
        self.assertTrue(generator.write_schema("test", SCHEMA))


if __name__ == '__main__':
    unittest.main()
