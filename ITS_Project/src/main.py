"""
Main Entry Point
Run this file to start the application
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from core.ontology_manager import OntologyManager
from ui.app import PythonIterationTutor


def main():
    """Main function to start the application"""
    print("=" * 60)
    print("🐍 PYTHON ITERATION TUTOR")
    print("=" * 60)
    print("\nInitializing...")
    
    # Get ontology path (one level up from src/)
    ontology_path = os.path.join(
        os.path.dirname(__file__), 
        '..', 
        'python_iteration_tutor.owl'
    )
    
    try:
        # Load ontology
        print(f"Loading ontology from: {ontology_path}")
        manager = OntologyManager(ontology_path)
        
        # Get stats
        stats = manager.get_statistics()
        print(f"\n✅ Ready!")
        print(f"   • {stats['concepts']} concepts loaded")
        print(f"   • {stats['problems']} problems available")
        print(f"   • {stats['test_cases']} test cases ready")
        print("\n" + "=" * 60)
        print("Starting GUI...\n")
        
        # Create and run application
        app = PythonIterationTutor(manager)
        app.run()
        
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: {e}")
        print("\nMake sure 'python_iteration_tutor.owl' is in the project root!")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()