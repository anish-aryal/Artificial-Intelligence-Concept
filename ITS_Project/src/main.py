"""
Main Entry Point - Start the application
"""

import sys
import os

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from src.core.ontology_manager import OntologyManager
from src.ui.app import PythonIterationTutor


def main():
    """Main function"""
    print("=" * 70)
    print("PYTHON ITERATION TUTOR - Professional ITS")
    print("=" * 70)
    print("\nInitializing system...")
    
    # Get ontology path (in project root)
    ontology_path = os.path.join(parent_dir, 'python_iteration_tutor.owl')
    
    try:
        # Load ontology
        print(f"Loading ontology...")
        manager = OntologyManager(ontology_path)
        
        # Get statistics
        stats = manager.get_statistics()
        print(f"\n✓ System Ready")
        print(f"  • {stats['concepts']} concepts loaded")
        print(f"  • {stats['problems']} problems available")
        print(f"  • {stats['solutions']} solutions ready")
        print(f"  • {stats['test_cases']} test cases configured")
        print("\n" + "=" * 70)
        print("Starting GUI...\n")
        
        # Create and run application
        app = PythonIterationTutor(manager)
        app.run()
        
    except FileNotFoundError as e:
        print(f"\n✕ ERROR: {e}")
        print("\nMake sure 'python_iteration_tutor.owl' is in the project root.")
        sys.exit(1)
    except Exception as e:
        print(f"\n✕ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()