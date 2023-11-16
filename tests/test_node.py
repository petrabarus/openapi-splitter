import unittest
import os
from openapi_splitter.node import Node
from openapi_splitter.io import read_yaml_from_file

dir_path = os.path.dirname(os.path.abspath(__file__)) + "/"


class TestNode(unittest.TestCase):
    def test_node(self):
        node = Node({})
        self.assertEqual(node.level, 0)

    def test_build(self):
        test_file = dir_path + "../res/test/sample2-input.yaml"
        yaml_input = read_yaml_from_file(test_file)
        node = Node(yaml_input)
        self.assertEqual(node.level, 0)
        self.assertEqual(len(node.children), 2)
