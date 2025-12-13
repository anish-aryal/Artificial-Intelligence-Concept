"""
Code Validator - Validates student Python code
Hybrid approach with Common Mistake Detection
"""

import ast
import io
import sys
import re
from contextlib import redirect_stdout, redirect_stderr


class CodeValidator:
    """Validates student code submissions with smart error detection"""
    
    def __init__(self):
        """Initialize validator"""
        self.timeout = 5
    
    def detect_common_mistakes(self, code, problem_concept=None):
        """
        Analyze code for common mistakes based on patterns
        
        Args:
            code: Student's code
            problem_concept: The concept being tested (e.g., 'BasicListIteration')
            
        Returns:
            List of detected mistake descriptions
        """
        detected = []
        code_stripped = code.strip()
        code_lower = code_stripped.lower()
        
        # Pattern 1: Missing colon at end of for statement
        for_lines = [line for line in code_stripped.split('\n') if line.strip().startswith('for ')]
        for line in for_lines:
            line_stripped = line.strip()
            if ' in ' in line_stripped and not line_stripped.endswith(':'):
                detected.append({
                    'type': 'missing_colon',
                    'message': "Missing colon (:) at the end of the for statement. Python requires a colon to start a code block.",
                    'line': line_stripped
                })
        
        # Pattern 2: Missing 'in' keyword
        for line in for_lines:
            if ' in ' not in line:
                detected.append({
                    'type': 'missing_in',
                    'message': "Missing 'in' keyword in for loop. Correct syntax: for item in collection:",
                    'line': line.strip()
                })
        
        # Pattern 3: Using index when not needed (for simple iteration)
        if problem_concept == 'BasicListIteration' or problem_concept == 'StringIteration':
            if '[i]' in code_stripped or '[index]' in code_stripped:
                if 'enumerate' not in code_lower:
                    detected.append({
                        'type': 'unnecessary_index',
                        'message': "Using index syntax when not needed. When iterating directly with 'for item in list', the item variable already contains the value.",
                        'line': None
                    })
        
        # Pattern 4: enumerate() without two variables
        if 'enumerate' in code_lower:
            # Check if there's a comma before 'in'
            enumerate_pattern = r'for\s+(\w+)\s+in\s+enumerate'
            if re.search(enumerate_pattern, code_lower):
                detected.append({
                    'type': 'enumerate_single_var',
                    'message': "enumerate() returns (index, value) tuples. You must unpack both: for i, item in enumerate(list)",
                    'line': None
                })
        
        # Pattern 5: .items() without two variables
        if '.items()' in code_lower:
            items_pattern = r'for\s+(\w+)\s+in\s+\w+\.items\(\)'
            if re.search(items_pattern, code_lower):
                detected.append({
                    'type': 'items_single_var',
                    'message': "dict.items() returns (key, value) tuples. You must unpack both: for key, value in dict.items()",
                    'line': None
                })
        
        # Pattern 6: Using .items() when .keys() or .values() is needed
        if problem_concept == 'DictKeysIteration' and '.items()' in code_lower:
            detected.append({
                'type': 'wrong_method',
                'message': "Use .keys() to iterate over dictionary keys only, not .items()",
                'line': None
            })
        
        if problem_concept == 'DictValuesIteration' and '.items()' in code_lower:
            detected.append({
                'type': 'wrong_method',
                'message': "Use .values() to iterate over dictionary values only, not .items()",
                'line': None
            })
        
        # Pattern 7: Incorrect indentation (no indented line after for)
        lines = code_stripped.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith('for ') and line.strip().endswith(':'):
                # Check if next line exists and is indented
                if i + 1 < len(lines):
                    next_line = lines[i + 1]
                    if next_line.strip() and not next_line.startswith((' ', '\t')):
                        detected.append({
                            'type': 'indentation',
                            'message': "Loop body must be indented. Python uses indentation to define code blocks (usually 4 spaces).",
                            'line': next_line.strip()
                        })
        
        return detected
        
    def validate_hybrid(self, student_code, solution_code, expected_output):
        """
        Hybrid validation - Check against BOTH solution and expected output
        """
        result = {
            'valid': False,
            'score': 0,
            'errors': [],
            'feedback': [],
            'warnings': [],
            'expected_output': expected_output,
            'solution_output': '',
            'actual_output': '',
            'detected_mistakes': []
        }
        
        # Step 1: Check syntax
        syntax_check = self._check_syntax(student_code)
        if not syntax_check['valid']:
            result['errors'] = syntax_check['errors']
            result['feedback'].append("Fix syntax errors before testing.")
            # Also check for common mistakes in syntax
            result['detected_mistakes'] = self.detect_common_mistakes(student_code)
            return result
        
        try:
            # Step 2: Run solution to get solution output
            solution_output = self._execute_code(solution_code)
            result['solution_output'] = solution_output
            
            # Step 3: Sanity check
            if solution_output.strip() != expected_output.strip():
                result['warnings'].append(
                    "Warning: Solution output doesn't match expected output."
                )
            
            # Step 4: Run student code
            student_output = self._execute_code(student_code)
            result['actual_output'] = student_output
            
            # Step 5: Compare outputs
            expected_lines = [line.strip() for line in expected_output.strip().split('\n')]
            solution_lines = [line.strip() for line in solution_output.strip().split('\n')]
            actual_lines = [line.strip() for line in student_output.strip().split('\n')]
            
            matches_expected = (expected_lines == actual_lines)
            matches_solution = (solution_lines == actual_lines)
            
            # Step 6: Determine result
            if matches_expected or matches_solution:
                result['valid'] = True
                result['score'] = 100
                result['feedback'].append("Perfect! Your code produces the correct output!")
            else:
                result['score'] = 0
                result['feedback'].append("Output doesn't match expected result.")
                # Detect common mistakes for failed submissions
                result['detected_mistakes'] = self.detect_common_mistakes(student_code)
        
        except Exception as e:
            result['errors'].append(f"Runtime Error: {str(e)}")
            result['feedback'].append("Your code produced an error.")
            result['detected_mistakes'] = self.detect_common_mistakes(student_code)
        
        return result
    
    def validate_with_test_cases(self, student_code, problem_details, solution_code):
        """
        Validate with multiple test cases using hybrid method
        """
        result = {
            'valid': False,
            'score': 0,
            'tests_passed': 0,
            'tests_total': 0,
            'errors': [],
            'feedback': [],
            'results': [],
            'detected_mistakes': []
        }
        
        # Check syntax first
        syntax_check = self._check_syntax(student_code)
        if not syntax_check['valid']:
            result['errors'] = syntax_check['errors']
            result['feedback'].append("Fix syntax errors before testing.")
            result['detected_mistakes'] = self.detect_common_mistakes(
                student_code, 
                problem_details.get('concept')
            )
            return result
        
        # Get test cases
        test_cases = problem_details.get('test_cases', [])
        result['tests_total'] = len(test_cases)
        
        if not test_cases:
            result['errors'].append("No test cases available.")
            return result
        
        # Run each test case
        for idx, test_case in enumerate(test_cases):
            test_result = self._run_hybrid_test(
                student_code, 
                solution_code,
                test_case, 
                idx + 1
            )
            result['results'].append(test_result)
            
            if test_result['passed']:
                result['tests_passed'] += 1
        
        # Calculate score
        if result['tests_total'] > 0:
            result['score'] = int((result['tests_passed'] / result['tests_total']) * 100)
            result['valid'] = result['score'] >= 70
        
        # Generate feedback
        if result['valid']:
            if result['score'] == 100:
                result['feedback'].insert(0, "Perfect! All tests passed!")
            else:
                result['feedback'].insert(0, f"Good job! Passed {result['tests_passed']}/{result['tests_total']} tests.")
        else:
            result['feedback'].insert(0, f"Keep trying! Only {result['tests_passed']}/{result['tests_total']} tests passed.")
            # Detect common mistakes for failed submissions
            result['detected_mistakes'] = self.detect_common_mistakes(
                student_code, 
                problem_details.get('concept')
            )
        
        return result
    
    def _run_hybrid_test(self, student_code, solution_code, test_case, test_number):
        """Run a single test with hybrid validation"""
        result = {
            'test_number': test_number,
            'description': test_case.get('description', f"Test {test_number}"),
            'passed': False,
            'expected': '',
            'actual': '',
            'solution_output': '',
            'error': None,
            'input_used': test_case.get('input', '')
        }
        
        try:
            test_input = test_case.get('input', '')
            expected_output = test_case.get('output', '').strip()
            
            # Run solution with test input
            solution_with_input = f"{test_input}\n{solution_code}"
            solution_output = self._execute_code(solution_with_input)
            result['solution_output'] = solution_output.strip()
            
            # Run student code with test input
            student_with_input = f"{test_input}\n{student_code}"
            student_output = self._execute_code(student_with_input)
            
            result['expected'] = expected_output
            result['actual'] = student_output.strip()
            
            # Compare outputs
            expected_lines = [line.strip() for line in expected_output.split('\n')]
            solution_lines = [line.strip() for line in solution_output.strip().split('\n')]
            actual_lines = [line.strip() for line in student_output.strip().split('\n')]
            
            matches_expected = (expected_lines == actual_lines)
            matches_solution = (solution_lines == actual_lines)
            
            result['passed'] = matches_expected or matches_solution
            
        except Exception as e:
            result['error'] = str(e)
            result['passed'] = False
        
        return result
    
    def _execute_code(self, code):
        """Execute code and return output"""
        output_buffer = io.StringIO()
        error_buffer = io.StringIO()
        
        safe_globals = {
            '__builtins__': {
                'print': print,
                'len': len,
                'range': range,
                'enumerate': enumerate,
                'str': str,
                'int': int,
                'float': float,
                'list': list,
                'dict': dict,
                'tuple': tuple,
                'set': set,
                'abs': abs,
                'max': max,
                'min': min,
                'sum': sum,
                'sorted': sorted,
                'reversed': reversed,
                'zip': zip,
                'map': map,
                'filter': filter,
                'round': round,
                'format': format
            }
        }
        
        with redirect_stdout(output_buffer), redirect_stderr(error_buffer):
            exec(code, safe_globals)
        
        error_output = error_buffer.getvalue()
        if error_output:
            raise Exception(error_output)
        
        return output_buffer.getvalue()
    
    def _check_syntax(self, code):
        """Check Python syntax"""
        try:
            ast.parse(code)
            return {'valid': True, 'errors': []}
        except SyntaxError as e:
            return {
                'valid': False,
                'errors': [f"Syntax Error on line {e.lineno}: {e.msg}"]
            }
        except Exception as e:
            return {
                'valid': False,
                'errors': [f"Parse Error: {str(e)}"]
            }