import ast
from typing import List, Dict, Optional


class CodeSmellDetector:
    """
    Detects code smells using AST parsing.
    """

    def __init__(self, max_function_length: int = 20, max_parameters: int = 5):
        self.max_function_length = max_function_length
        self.max_parameters = max_parameters
        pass

    def analyze_code(self, source_code: str) -> List[Dict]:
        """
        Args:
            source_code: Python code in a String format

        Returns:
            List of Dict with informations about code smells
        """

        smells = []

        try:
            tree = ast.parse(source_code)

            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    smell = self._check_function(node)
                    if smell:
                        smells.append(smell)
                elif isinstance(node, ast.ClassDef):
                    smell = self._check_class(node)
                    if smell:
                        smells.append(smell)

        except SyntaxError as e:
            smells.append(
                {
                    "type": "SyntaxError",
                    "message": f"Syntax error: {str(e)}",
                    "line": e.lineno,
                }
            )

        return smells


    def _check_function(self, node: ast.FunctionDef) -> Optional[Dict]:


        function_length = len(node.body)

        num_params = len(node.args.args)

        if function_length > self.max_function_length:
            return {
                "type": "LongFunction",
                "name": node.name,
                "line": node.lineno,
                "message": f"Function {node.name} has {function_length} statements (recommended: max {self.max_function_length})",
                "severity": "medium",  # Pentru ML classifier
            }

        if num_params > self.max_parameters:
            return {
                "type": "TooManyParameters",
                "name": node.name,
                "line": node.lineno,
                "message": f"Function {node.name} has {num_params} parameters (recommended: max {self.max_parameters})",
                "severity": "low",
            }

        return None


    def _check_class(self, node: ast.ClassDef) -> Optional[Dict]:

        num_methods = sum(1 for n in node.body if isinstance(n, ast.FunctionDef))

        if num_methods > 15:
            return {
                "type": "GodClass",
                "name": node.name,
                "line": node.lineno,
                "message": f"Class {node.name} has {num_methods} methods (possible God Class)",
                "severity": "high",
            }

        return None
