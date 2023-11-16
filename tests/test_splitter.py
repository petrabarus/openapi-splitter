import unittest
import os
from dataclasses import dataclass
from openapi_splitter.splitter import Splitter
from openapi_splitter.io import read_yaml_from_file
import tempfile

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"


class TestSplitter(unittest.TestCase):
    def test_splitter(self):
        splitter = Splitter({}, "")
        self.assertEqual(splitter.yaml, {})

    def test_split(self):
        @dataclass
        class TestCase:
            name: str
            input_file: str
            expected_output_document_count: int

        test_cases = [
            TestCase("test 1", "../res/samples/petstore-simple.yaml", 4),
            # TestCase("test 2", "../res/samples/petstore-expanded.yaml"),
        ]

        for test_case in test_cases:
            file_path = dir_path + test_case.input_file
            input_yaml = read_yaml_from_file(file_path)
            temp_dir = tempfile.TemporaryDirectory()

            splitter = Splitter(input_yaml, temp_dir.name)
            splitter.verbose = True
            splitter.split()
            # print(splitter.root)
            self.assertEqual(len(splitter.output_documents),
                             test_case.expected_output_document_count)
