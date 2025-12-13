"""
Ontology Manager - Handles loading and querying the OWL ontology
Provides clean interface to access concepts, problems, solutions, and test cases
"""

from owlready2 import *
import os
import logging

# Configure logging for debugging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


class OntologyManager:
    """Manages all interactions with the ontology"""
    
    def __init__(self, ontology_path):
        """Load ontology from file path"""
        self.ontology_path = ontology_path
        self.onto = None
        self._load_ontology()
    
    def _load_ontology(self):
        """Load and validate ontology file"""
        try:
            # Verify file exists
            if not os.path.exists(self.ontology_path):
                raise FileNotFoundError(f"❌ Ontology file not found: {self.ontology_path}")
            
            # Load using OWLready2
            logger.info(f"Loading ontology from: {self.ontology_path}")
            self.onto = get_ontology(f"file://{self.ontology_path}").load()
            logger.info("✅ Ontology loaded successfully!")
            
        except FileNotFoundError as e:
            logger.error(str(e))
            raise
        except Exception as e:
            logger.error(f"❌ Error loading ontology: {e}")
            raise
    
    def get_concepts(self):
        """Return all IterationConcept instances"""
        try:
            concepts = list(self.onto.IterationConcept.instances())
            logger.info(f"Retrieved {len(concepts)} concepts")
            return concepts
        except Exception as e:
            logger.error(f"Error getting concepts: {e}")
            return []
    
    def get_problems(self):
        """
        Get all problems regardless of difficulty
        Returns list of Problem instances
        """
        try:
            problems = list(self.onto.Problem.instances())
            logger.info(f"Retrieved {len(problems)} problems")
            return problems
        except Exception as e:
            logger.error(f"Error getting problems: {e}")
            return []
    
    def get_concept_details(self, concept):
        """
        Extract all details for a concept
        Returns dict with: name, explanation, syntax, code, iterable, method
        """
        try:
            details = {
                'name': concept.name,
                'explanation': self._get_property(concept, 'explanation'),
                'syntax': self._get_property(concept, 'syntaxPattern'),
                'code': self._get_property(concept, 'codeExample'),
                'iterable': None,
                'method': None
            }
            
            # Get linked iterable (List, String, Dictionary)
            if hasattr(concept, 'hasIterable') and concept.hasIterable:
                iterable = concept.hasIterable[0]
                details['iterable'] = {
                    'name': iterable.name,
                    'explanation': self._get_property(iterable, 'iterableExplanation')
                }
            
            # Get linked method (ForLoop, Enumerate, Items, etc.)
            if hasattr(concept, 'hasMethod') and concept.hasMethod:
                method = concept.hasMethod[0]
                details['method'] = {
                    'name': method.name,
                    'explanation': self._get_property(method, 'methodExplanation')
                }
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting concept details: {e}")
            return None
    
    def get_problems_by_level(self, level):
        """
        Get problems filtered by difficulty (1=easy, 2=medium, 3=hard)
        Returns list of Problem instances
        """
        try:
            all_problems = list(self.onto.Problem.instances())
            
            # Filter where difficultyLevel matches requested level
            filtered = [
                p for p in all_problems 
                if hasattr(p, 'difficultyLevel') and p.difficultyLevel[0] == level
            ]
            
            logger.info(f"Found {len(filtered)} problems at level {level}")
            return filtered
            
        except Exception as e:
            logger.error(f"Error getting problems: {e}")
            return []
    
    def get_problem_details(self, problem):
        """
        Extract all details for a problem
        Returns dict with: name, description, hint, difficulty, concept, test_cases, expected_output, starter_code
        """
        try:
            details = {
                'name': problem.name,
                'description': self._get_property(problem, 'problemDescription'),
                'hint': self._get_property(problem, 'hint') or 'Try breaking the problem into smaller steps.',
                'difficulty': self._get_int_property(problem, 'difficultyLevel') or 1,
                'concept': None,
                'test_cases': [],
                'expected_output': '',
                'starter_code': '# Write your code here\n'
            }
            
            # Get required concept name
            if hasattr(problem, 'requiresConcept') and problem.requiresConcept:
                concept = problem.requiresConcept[0]
                details['concept'] = concept.name
            
            # Get all linked test cases (input/output pairs)
            if hasattr(problem, 'hasTestCase') and problem.hasTestCase:
                for tc in problem.hasTestCase:
                    test_case = {
                        'description': self._get_property(tc, 'testDescription') or f"Test {len(details['test_cases']) + 1}",
                        'input': self._get_property(tc, 'testInput') or '',
                        'output': self._get_property(tc, 'testOutput') or ''
                    }
                    details['test_cases'].append(test_case)
                    
                    # Set expected output from first test case
                    if not details['expected_output'] and test_case['output']:
                        details['expected_output'] = test_case['output']
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting problem details: {e}")
            return None
    
    def get_common_mistakes(self, problem=None):
        """
        Get common mistakes, optionally filtered by problem
        Returns list of mistake dicts with: name, message
        """
        try:
            if problem and hasattr(problem, 'hasMistake') and problem.hasMistake:
                # Get mistakes linked to this problem
                mistakes = []
                for mistake in problem.hasMistake:
                    mistakes.append({
                        'name': mistake.name,
                        'message': self._get_property(mistake, 'errorMessage')
                    })
                return mistakes
            else:
                # Get all mistakes if no problem specified
                all_mistakes = list(self.onto.CommonMistake.instances())
                return [
                    {
                        'name': m.name,
                        'message': self._get_property(m, 'errorMessage')
                    }
                    for m in all_mistakes
                ]
        except Exception as e:
            logger.error(f"Error getting common mistakes: {e}")
            return []

    def get_all_test_cases(self, problem):
        """
        Get all test cases for a problem with full details
        Returns list of test case dicts
        """
        try:
            test_cases = []
            if hasattr(problem, 'hasTestCase') and problem.hasTestCase:
                for tc in problem.hasTestCase:
                    test_cases.append({
                        'name': tc.name,
                        'description': self._get_property(tc, 'testDescription') or f"Test {len(test_cases) + 1}",
                        'input': self._get_property(tc, 'testInput') or '',
                        'output': self._get_property(tc, 'testOutput') or ''
                    })
            return test_cases
        except Exception as e:
            logger.error(f"Error getting test cases: {e}")
            return []
    def get_solution(self, problem):
        """
        Find solution for given problem
        Returns dict with: code, output (or None if not found)
        """
        try:
            # Search through all solutions to find match
            for solution in self.onto.Solution.instances():
                if hasattr(solution, 'solvesProblem') and solution.solvesProblem:
                    if solution.solvesProblem[0] == problem:
                        return {
                            'code': self._get_property(solution, 'solutionCode'),
                            'output': self._get_property(solution, 'expectedOutput')
                        }
            
            logger.warning(f"No solution found for {problem.name}")
            return None
            
        except Exception as e:
            logger.error(f"Error getting solution: {e}")
            return None
    
    def _get_int_property(self, instance, property_name):
        """
        Safely extract integer property value
        Returns integer or None if property doesn't exist
        """
        value = self._get_property(instance, property_name)
        if value is not None:
            return int(value)  # Convert float to int
        return None
    
    def _get_property(self, instance, property_name):
        """
        Safely extract property value from ontology instance
        Returns first value or None if property doesn't exist
        """
        try:
            if hasattr(instance, property_name):
                prop_value = getattr(instance, property_name)
                if prop_value:
                    return prop_value[0]  # OWLready2 stores properties as lists
            return None
        except Exception as e:
            logger.warning(f"Could not get property '{property_name}': {e}")
            return None
    
    def get_statistics(self):
        """
        Count all ontology elements
        Returns dict with: concepts, problems, solutions, test_cases
        """
        try:
            return {
                'concepts': len(list(self.onto.IterationConcept.instances())),
                'problems': len(list(self.onto.Problem.instances())),
                'solutions': len(list(self.onto.Solution.instances())),
                'test_cases': len(list(self.onto.TestCase.instances()))
            }
        except Exception as e:
            logger.error(f"Error getting statistics: {e}")
            return {'concepts': 0, 'problems': 0, 'solutions': 0, 'test_cases': 0}