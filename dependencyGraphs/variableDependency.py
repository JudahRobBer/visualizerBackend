"""
Module generates a networkx formatted, serializable graph structure to be fed to the front end through the api
"""

import ast
import networkx as nx
from pprint import pprint



class VariableDependencyVisitor(ast.NodeVisitor):
    def __init__(self):
        #an edge represents a dependency: x -> y : x depends on y
        self.graph = nx.DiGraph()
        self.printed_variables = set()
        self.inputed_variables = set()
        self.current_function = None
        self.variable_function_location = {}
    

    # Graph Exportation  -------------------------------------------------------------

    def return_serialized_labeled_graph(self):
        self.label_nodes()
        json_graph = nx.json_graph.node_link_data(self.graph)
        
        #filter json object
        valid_keys = ['links','nodes']
        reduced_graph = {key:json_graph[key] for key in valid_keys}
        return reduced_graph
    
    # Variable Dependency Identification and Graph Initializition ---------------------------------

    def visit_Assign(self,node) -> None:
        targets = []
        for target in node.targets:
            if isinstance(target,ast.Subscript):
                targets.append(target.value.id)
            else: #name case
                targets.append(target.id)
        
        self._update_graph(node,targets)
        
        self.generic_visit(node)   

     
    def visit_AnnAssign(self,node):
        targets = self._build_targets(node)
        
        self._update_graph(node,targets)
        self.generic_visit(node)

    
    def visit_AugAssign(self,node):
        targets = self._build_targets(node)

        self._update_graph(node,targets)
        self.generic_visit(node)


    def _build_targets(self,node):
        if isinstance(node.target,ast.Subscript):
            targets = [node.target.value.id]
        elif isinstance(node.target,ast.Name):
            targets = [node.target.id]
        return targets


    def _update_graph(self,node,targets):
        self._match_value_type(node,targets) #edges
        for target in targets: #nodes
            self.graph.add_node(target)
            self.variable_function_location[target] = self.current_function #labeling
    
    
    def _match_value_type(self,node,targets):
        match type(node.value):
            case ast.Name:
                for target in targets:
                    self.graph.add_edge(target,node.value.id)
            case ast.Call:
                #identify all the arguments in the function call
                self._find_inputed_variables(node.value,targets)
                args = self._extract_function_arguments(node.value)
                for target in targets:
                    for arg in args:
                        self.graph.add_edge(target,arg)
            case ast.BinOp: 
                terms = self._flatten_binOP(node.value)
                for target in targets:
                    for term in terms:
                        self.graph.add_edge(target,term)
            case ast.Subscript:
                #value refers to the object being subscripted
                self._match_value_type(node.value,targets)
            case None:
                return
    
    
    def _flatten_binOP(self,node) -> list:
        #recursive tree exploration
        terms = []
        match type(node):
            case ast.BinOp:
                terms += self._flatten_binOP(node.left)
                terms += self._flatten_binOP(node.right)
            case ast.Name:
                terms.append(node.id)

        return terms
    
    
    def _extract_function_arguments(self,node) -> list:
        args = []
        for arg in node.__dict__["args"]:
            match type(arg):
                case ast.BinOp:
                    args.extend(self._flatten_binOP(arg))
                case ast.Name:
                    args.append(arg.id)
                case ast.Call:
                    args.extend(self._extract_function_arguments(arg))
        return args
    

    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.current_function = node.name
        self.generic_visit(node)
    

    # Label Dependency Graph Nodes ----------------------------------------------------------------


    def label_nodes(self):
        attributes = {variable : {"Input":False,"Printed":False,"Function":None} for variable in self.graph.nodes()}
        self._label_printed_nodes(attributes)
        self._label_inputed_nodes(attributes)
        self._label_function_origin(attributes)
        nx.set_node_attributes(self.graph,attributes)

    
    def _label_printed_nodes(self,attributes:dict) -> None:
        for variable in self.printed_variables:
            attributes[variable]["Printed"] = True

    
    def _label_inputed_nodes(self,attributes:dict) -> None:
        for variable in self.inputed_variables:
            attributes[variable]["Input"] = True

    
    def _label_function_origin(self,attributes) -> None:
        for node, func in self.variable_function_location.items():
            attributes[node]["Function"] = func



    def visit_Call(self,node) -> None:
        try:
            if node.func.id == "print":
                self.printed_variables.update(self._extract_function_arguments(node))
        except Exception:
            pass
        
        self.generic_visit(node)


    def _find_inputed_variables(self,node,targets:list) -> None:
        for arg in node.__dict__["args"]:
            if isinstance(arg,ast.Call):
                if arg.func.id == "input":
                    self.inputed_variables.update(targets)

    
    

def create_vdg(source:str) -> dict:
    
    tree = ast.parse(source)

    visitor = VariableDependencyVisitor()
    visitor.visit(tree)
    graph = visitor.return_serialized_labeled_graph()
    return graph 
