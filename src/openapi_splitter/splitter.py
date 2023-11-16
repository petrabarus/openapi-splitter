"""
This module contains the Splitter class.
"""
import os
from os.path import relpath
from dataclasses import dataclass
from .node import Node, NodeKind


@dataclass
class OutputDocument:
    """
    This class represents an output document.
    """
    filename: str = None
    yaml: dict = None


@dataclass
class Ref:
    """
    This class represents a reference.
    """
    path: str = None
    node: Node = None
    filename: str = None


@dataclass
class Splitter:
    """
    This class represents a splitter that splits the OpenAPI specification
    file into multiple files.
    """
    yaml: dict = None
    root: Node = None
    output_dir: str = None
    verbose = False
    output_documents: list[OutputDocument] = None
    refs: dict[str, Ref] = None

    def __init__(self, yaml: dict, output_dir: str):
        self.yaml = yaml
        self.output_dir = output_dir
        self.output_documents = []
        self.refs = {}

    def split(self):
        """
        Split the OpenAPI specification file into multiple files.
        """
        root_node = Node(self.yaml, self.preprocess_node,
                         self.postprocess_node,
                         kind=NodeKind.DOCUMENT,
                         level=0)
        self.root = root_node
        main_yaml = self.root.rebuild_children_yaml()
        root_document = OutputDocument("main.yaml", main_yaml)
        self.output_documents.append(root_document)

        self.fix_local_references_in_output_documents()

    def preprocess_node(self, node: Node):
        """
        Pre-processes a node.

        :param node: The node to pre-process.
        """
        if node.kind != NodeKind.DOCUMENT:
            node.determine_kind()

    def postprocess_node(self, node: Node):
        """
        Post-processes a node.

        :param node: The node to post-process.
        """
        if node.kind == NodeKind.DOCUMENT:
            pass
        elif node.kind == NodeKind.PATH:
            self.process_path_node(node)
        elif node.kind == NodeKind.COMPONENTS_SCHEMA:
            self.process_components_schema_node(node)
        elif node.kind == NodeKind.COMPONENTS_PARAMETER:
            self.process_components_parameter_node(node)
        elif node.kind == NodeKind.COMPONENTS_SECURITY_SCHEME:
            self.process_components_security_scheme_node(node)
        elif node.kind == NodeKind.COMPONENTS_HEADER:
            self.process_components_header_node(node)
        elif node.kind == NodeKind.REF:
            self.process_ref_node(node)
        else:
            pass

    def process_path_node(self, node: Node):
        # Replace {} with __
        document_path = "paths" + \
            node.name.replace("{", "__").replace("}", "__") + \
            "/index.yaml"
        yaml = node.rebuild_children_yaml()
        output_document = OutputDocument(document_path, yaml)
        self.output_documents.append(output_document)

        ref_path = "./" + document_path
        node.create_ref_node(ref_path)
        pass

    def process_components_schema_node(self, node: Node):
        path = "components/schemas/" + node.name
        self.process_component_node(node, path)

    def process_components_parameter_node(self, node: Node):
        path = "components/parameters/" + node.name
        self.process_component_node(node, path)

    def process_components_security_scheme_node(self, node: Node):
        path = "components/securitySchemes/" + node.name
        self.process_component_node(node, path)

    def process_components_header_node(self, node: Node):
        path = "components/headers/" + node.name
        self.process_component_node(node, path)

    def process_ref_node(self, node: Node):
        pass

    def process_component_node(self, node: Node, path):
        ref_path = "#/" + path
        if ref_path not in self.refs:
            document_path = path + ".yaml"
            ref = Ref(ref_path, node, document_path)
            self.refs[ref_path] = ref
            yaml = node.rebuild_children_yaml()
            output_document = OutputDocument(document_path, yaml)
            self.output_documents.append(output_document)
            doc_ref_path = "./" + document_path
            node.create_ref_node(doc_ref_path)
        else:
            ref = self.refs[ref_path]
            node.create_ref_node(ref.filename)

    def fix_local_references_in_output_documents(self):
        """
        This will detect any local references, i.e. references that are
        started with #, and change them with location to the output document.
        """
        for output_document in self.output_documents:
            yaml = output_document.yaml
            filename = output_document.filename
            self.fix_local_references_in_yaml(yaml, filename)

    def fix_local_references_in_yaml(self, yaml: dict, src_filename: str):
        """
        This will detect any local references, i.e. references that are
        started with #, and change them with location to the output document.

        :param yaml: The YAML to fix.
        """
        if isinstance(yaml, dict):
            for key, value in yaml.items():
                if key == "$ref" and value.startswith("#"):
                    newvalue = \
                        self.replace_local_ref_with_target_ref(
                            value,
                            src_filename)
                    yaml[key] = newvalue
                else:
                    self.fix_local_references_in_yaml(value, src_filename)
        elif isinstance(yaml, list):
            for item in yaml:
                self.fix_local_references_in_yaml(item, src_filename)

    def replace_local_ref_with_target_ref(self,
                                          local_ref: str,
                                          src_filename: str) -> str:
        if local_ref in self.refs:
            ref = self.refs[local_ref]
            dst_filename = ref.filename
            return create_relative_path(src_filename, dst_filename)
        return local_ref


def create_relative_path(src: str, dest: str) -> str:
    """
    Create a relative path from src to dest.

    :param src: The source path.
    :param dest: The destination path.
    :return: The relative path from src to dest.
    """
    dir_path = os.path.dirname(__file__)
    src_abs_path = dir_path + "/" + src
    dest_abs_path = dir_path + "/" + dest
    result = "./" + relpath(
        dest_abs_path,
        os.path.dirname(src_abs_path)
    )
    # print("\tpath\n\t\t{}\n\t\t{}\n\t\t{}".format(src_abs_path,
    #                                               dest_abs_path, result))
    return result
