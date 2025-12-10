"""
Code Validator - Validates student Python code
Hybrid approach: Checks against BOTH solution and expected output
"""

import ast
import io
import sys
from contextlib import redirect_stdout, redirect_stderr


class CodeValidator:
    """Validates student code submissions - Hybrid Method"""
    
    def __init__(self):
        """Initialize validator"""
        self.timeout = 5
        
    def validate_hybrid(self, student_code, solution_code, expected_output):
        """
        Hybrid validation - Check against BOTH solution and expected output
        
        Args:
            student_code: Student's code
            solution_code: Correct solution code
            expected_output: Expected output from test case
            
        Returns:
            dict with validation results
        """
        result = {
            'valid': False,
            'score': 0,
            'errors': [],
            'feedback': [],
            'warnings': [],
            'expected_output': expected_output,
            'solution_output': '',
            'actual_output': ''
        }
        
        # Step 1: Check syntax
        syntax_check = self._check_syntax(student_code)
        if not syntax_check['valid']:
            result['errors'] = syntax_check['errors']
            result['feedback'].append("Fix syntax errors before testing.")
            return result
        
        try:
            # Step 2: Run solution to get solution output
            solution_output = self._execute_code(solution_code)
            result['solution_output'] = solution_output
            
            # Step 3: Sanity check - Verify solution matches expected output
            if solution_output.strip() != expected_output.strip():
                result['warnings'].append(
                    "⚠️ Warning: Solution output doesn't match expected output. "
                    "There may be an issue with the test case data."
                )
            
            # Step 4: Run student code
            student_output = self._execute_code(student_code)
            result['actual_output'] = student_output
            
            # Step 5: Compare student output with BOTH expected and solution
            expected_lines = [line.strip() for line in expected_output.strip().split('\n')]
            solution_lines = [line.strip() for line in solution_output.strip().split('\n')]
            actual_lines = [line.strip() for line in student_output.strip().split('\n')]
            
            matches_expected = (expected_lines == actual_lines)
            matches_solution = (solution_lines == actual_lines)
            
            # Step 6: Determine result
            if matches_expected and matches_solution:
                # Perfect! Matches both
                result['valid'] = True
                result['score'] = 100
                result['feedback'].append("Perfect! Your code produces the correct output!")
            elif matches_expected or matches_solution:
                # Matches one but not the other (edge case)
                result['valid'] = True
                result['score'] = 100
                result['feedback'].append("Correct! Your output matches the expected result.")
                if not matches_solution:
                    result['warnings'].append(
                        "Note: Your output differs slightly from the model solution but is still correct."
                    )
            else:
                # Doesn't match either
                result['score'] = 0
                result['feedback'].append("Output doesn't match expected result. Review your code.")
        
        except Exception as e:
            result['errors'].append(f"Runtime Error: {str(e)}")
            result['feedback'].append("Your code produced an error.")
        
        return result
    
    def validate_with_test_cases(self, student_code, problem_details, solution_code):
        """
        Validate with multiple test cases using hybrid method
        
        Args:
            student_code: Student's code
            problem_details: Dict with test cases
            solution_code: Solution code
            
        Returns:
            dict with validation results
        """
        result = {
            'valid': False,
            'score': 0,
            'tests_passed': 0,
            'tests_total': 0,
            'errors': [],
            'feedback': [],
            'results': []
        }
        
        # Check syntax first
        syntax_check = self._check_syntax(student_code)
        if not syntax_check['valid']:
            result['errors'] = syntax_check['errors']
            result['feedback'].append("Fix syntax errors before testing.")
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
            'error': None
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
            
            # Compare - student should match BOTH expected and solution
            expected_lines = [line.strip() for line in expected_output.split('\n')]
            solution_lines = [line.strip() for line in solution_output.strip().split('\n')]
            actual_lines = [line.strip() for line in student_output.strip().split('\n')]
            
            matches_expected = (expected_lines == actual_lines)
            matches_solution = (solution_lines == actual_lines)
            
            # Pass if matches either (with preference for expected)
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
                'set': set
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