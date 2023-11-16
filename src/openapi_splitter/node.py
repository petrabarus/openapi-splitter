"""
This module contains the Node class that represents a node in the tree of
the of YML node of the OpenAPI specification.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Callable


class NodeKind(Enum):
    """
    This class represents the kind of a node in the tree of the YML node of
    the OpenAPI specification.
    """
    UNDEFINED = 0
    DOCUMENT = 1
    UNKNOWN = 2
    PATHS_ROOT = 3
    PATH = 4
    REF = 5
    COMPONENTS_ROOT = 6
    COMPONENTS_SCHEMAS_ROOT = 7
    COMPONENTS_SCHEMA = 8
    COMPONENTS_PARAMETERS_ROOT = 9
    COMPONENTS_PARAMETER = 10
    COMPONENTS_SECURITY_SCHEMES_ROOT = 11
    COMPONENTS_SECURITY_SCHEME = 12
    COMPONENTS_HEADERS_ROOT = 13
    COMPONENTS_HEADER = 14
    PATH_OPERATION = 15
    PATH_OPERATION_RESPONSES_ROOT = 16
    PATH_OPERATION_RESPONSE = 17
    PATH_OPERATION_RESPONSE_BODY = 18


@dataclass
class Node:
    """
    This class represents a node in the tree of the of YML node of the
    OpenAPI specification.
    """
    # If map, this is the key. If list this will be empty.
    name: str = None
    # If list this is the value. If map this will be empty.
    # If string this is the value.
    value = None
    level: int = 0
    kind = NodeKind.UNDEFINED
    parent: 'Node' = None
    prev_sibling: 'Node' = None
    children: list['Node'] = None

    def __init__(self,
                 yaml,
                 preproc: Callable = None,
                 postproc: Callable = None,
                 name: str = None,
                 level: int = 0,
                 kind: NodeKind = NodeKind.UNDEFINED,
                 parent: 'Node' = None,
                 sibling: 'Node' = None):
        self.children = []
        self.name = name
        self.level = level
        self.kind = kind
        self.parent = parent
        self.prev_sibling = sibling

        self.build(yaml, preproc, postproc)

    def build(self, yaml, preproc: Callable = None, postproc: Callable = None):
        # print("processing yaml: {}".format(yaml))
        """
        Builds the node and applies pre-processing and post-processing
        functions if provided.

        :param preproc: A callable function to apply pre-processing to the
                        node.
        :param postproc: A callable function to apply post-processing to
                        the node.
        """
        if preproc:
            try:
                preproc(self)
            except Exception as exc:
                raise RuntimeError("preproc failed") from exc

        if isinstance(yaml, dict):
            for key, value in yaml.items():
                sibling = self.children[-1] if len(self.children) > 0 else None
                child_node = Node(value, preproc, postproc,
                                  name=key,
                                  level=self.level + 1,
                                  parent=self,
                                  sibling=sibling)
                child_node.prev_sibling = self.children[-1] \
                    if len(self.children) > 0 else None
                self.children.append(child_node)
        elif isinstance(yaml, list):
            for item in yaml:
                sibling = self.children[-1] if len(self.children) > 0 else None
                child_node = Node(item, preproc, postproc,
                                  level=self.level + 1,
                                  parent=self,
                                  sibling=sibling)
                self.children.append(child_node)
            pass
        elif is_scalar(yaml):
            self.value = yaml
            if is_node_ref(self):
                self.kind = NodeKind.REF

        if postproc:
            try:
                postproc(self)
            except Exception as exc:
                raise RuntimeError("postproc failed") from exc

    def create_ref_node(self, ref: str):
        """
        Creates a reference node.

        :param ref: The reference.
        """
        ref_yaml = {"$ref": ref}
        ref_node = Node(ref_yaml, name="$ref", level=self.level)
        self.children = ref_node.children
        for child in self.children:
            child.parent = self

    def rebuild_yaml(self):
        """
        Rebuilds the YAML from the children.
        """
        if self.name:
            if is_scalar(self.value):
                return {self.name: self.value}
            return {self.name: self.rebuild_children_yaml()}
        else:
            result = []
            for child in self.children:
                result.append(child.rebuild_yaml())
            return result

    def rebuild_children_yaml(self):
        """
        Rebuilds the YAML from the children.
        """
        result_dict = {}
        result_list = []
        for child in self.children:
            if child.name:
                if is_scalar(child.value):
                    result_dict[child.name] = child.value
                else:
                    result_dict[child.name] = child.rebuild_children_yaml()
            elif child.value:
                result_list.append(child.value)
            else:
                result_list.append(child.rebuild_children_yaml())
        if len(result_dict) > 0:
            return result_dict
        else:
            return result_list

    def __str__(self):
        result = ""
        tab = "\t" * self.level

        result += f"{tab}kind: {self.kind}\n"
        result += f"{tab}level: {self.level}\n"
        result += f"{tab}name: {self.name}\n"
        result += f"{tab}value: {self.value}\n"
        if len(self.children) > 0:
            result += f"{tab}children:\n"
            for child in self.children:
                result += str(child)
        else:
            result += "\n"

        return result

    def determine_kind(self) -> NodeKind:
        """
        Determines the kind of the node.
        """
        self.kind = determine_node_kind(self)
        return self.kind


def is_scalar(yaml) -> bool:
    return isinstance(yaml, str) or \
        isinstance(yaml, int) or \
        isinstance(yaml, float) or \
        isinstance(yaml, bool)


def determine_node_kind(n: Node) -> NodeKind:
    determiner = NodeKindDeterminer(n)
    return determiner.determine_kind()


def is_node_ref(n: Node) -> bool:
    determiner = NodeKindDeterminer(n)
    return determiner.is_ref()


@dataclass
class NodeKindDeterminer:
    node: Node = None
    """
    This class determines the kind of a node.
    """

    def __init__(self, node: Node):
        self.node = node

    def determine_kind(self) -> NodeKind:
        if self.is_paths_root():
            return NodeKind.PATHS_ROOT
        elif self.is_path():
            return NodeKind.PATH
        elif self.is_ref():
            return NodeKind.REF
        elif self.is_components_root():
            return NodeKind.COMPONENTS_ROOT
        elif self.is_components_schemas_root():
            return NodeKind.COMPONENTS_SCHEMAS_ROOT
        elif self.is_components_schema():
            return NodeKind.COMPONENTS_SCHEMA
        elif self.is_components_parameters_root():
            return NodeKind.COMPONENTS_PARAMETERS_ROOT
        elif self.is_components_parameter():
            return NodeKind.COMPONENTS_PARAMETER
        elif self.is_components_security_schemes_root():
            return NodeKind.COMPONENTS_SECURITY_SCHEMES_ROOT
        elif self.is_components_security_scheme():
            return NodeKind.COMPONENTS_SECURITY_SCHEME
        elif self.is_components_headers_root():
            return NodeKind.COMPONENTS_HEADERS_ROOT
        elif self.is_components_header():
            return NodeKind.COMPONENTS_HEADER
        elif self.is_path_operation():
            return NodeKind.PATH_OPERATION
        elif self.is_path_operation_responses_root():
            return NodeKind.PATH_OPERATION_RESPONSES_ROOT
        else:
            return NodeKind.UNKNOWN

    def is_paths_root(self):
        """
        Determines if the node is the root of the paths.
        """
        n = self.node
        return n.level == 1 and \
            n.name and \
            n.name == "paths" and \
            n.parent and \
            n.parent.kind == NodeKind.DOCUMENT

    def is_path(self):
        """
        Determines if the node is a path, e.g. /pets.
        """
        n = self.node
        return n.level == 2 and \
            n.parent and \
            n.parent.kind == NodeKind.PATHS_ROOT

    def is_ref(self):
        """
        Determines if the node is a reference.
        """
        n = self.node
        return n.name == "$ref" and \
            isinstance(n.value, str)

    def is_components_root(self):
        """
        Determines if the node is the root of the components.
        """
        n = self.node
        return n.level == 1 and \
            n.name and \
            n.name == "components" and \
            n.parent and \
            n.parent.kind == NodeKind.DOCUMENT

    def is_components_schemas_root(self):
        """
        Determines if the node is the root of the schemas.
        """
        n = self.node
        return n.level == 2 and \
            n.name and \
            n.name == "schemas" and \
            n.parent and \
            n.parent.kind == NodeKind.COMPONENTS_ROOT

    def is_components_schema(self):
        """
        Determines if the node is a schema.
        """
        n = self.node
        return n.level == 3 and \
            n.parent and \
            n.parent.kind == NodeKind.COMPONENTS_SCHEMAS_ROOT

    def is_components_parameters_root(self):
        """
        Determines if the node is the root of the parameters.
        """
        n = self.node
        return n.level == 2 and \
            n.name and \
            n.name == "parameters" and \
            n.parent and \
            n.parent.kind == NodeKind.COMPONENTS_ROOT

    def is_components_parameter(self):
        """
        Determines if the node is a parameter.
        """
        n = self.node
        return n.level == 3 and \
            n.parent and \
            n.parent.kind == NodeKind.COMPONENTS_PARAMETERS_ROOT

    def is_components_security_schemes_root(self):
        """
        Determines if the node is the root of the security schemes.
        """
        n = self.node
        return n.level == 2 and \
            n.name and \
            n.name == "securitySchemes" and \
            n.parent and \
            n.parent.kind == NodeKind.COMPONENTS_ROOT

    def is_components_security_scheme(self):
        """
        Determines if the node is a security scheme.
        """
        n = self.node
        return n.level == 3 and \
            n.parent and \
            n.parent.kind == NodeKind.COMPONENTS_SECURITY_SCHEMES_ROOT

    def is_components_headers_root(self):
        """
        Determines if the node is the root of the security headers.
        """
        n = self.node
        return n.level == 2 and \
            n.name and \
            n.name == "headers" and \
            n.parent and \
            n.parent.kind == NodeKind.COMPONENTS_ROOT

    def is_components_header(self):
        """
        Determines if the node is a security header.
        """
        n = self.node
        return n.level == 3 and \
            n.parent and \
            n.parent.kind == NodeKind.COMPONENTS_HEADERS_ROOT

    def is_path_operation(self):
        """
        Determines if the node is a path operation, e.g. get.
        """
        n = self.node
        eligible_names = [
            "get", "put", "post", "delete", "options", "head",
            "patch", "trace"]
        return n.level == 3 and \
            n.name and \
            n.name in eligible_names and \
            n.parent and \
            n.parent.kind == NodeKind.PATH

    def is_path_operation_responses_root(self):
        """
        Determines if the node is the root of the responses.
        """
        n = self.node
        return n.level == 4 and \
            n.name and \
            n.name == "responses" and \
            n.parent and \
            n.parent.kind == NodeKind.PATH_OPERATION
