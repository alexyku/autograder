import unittest
import sys
import os
import shutil
from nbconvert import PythonExporter

def main(notebook_path):
    """
    Grades a single notebook file by converting it and running unit tests.
    """
    # Define the name for the temporary script
    temp_script_path = "student_code.py"
    
    # Ensure the __pycache__ and student_code module are clean before starting
    if os.path.exists("__pycache__"):
        shutil.rmtree("__pycache__")
    if "student_code" in sys.modules:
        del sys.modules["student_code"]

    try:
        # 1. Convert the specified notebook to a Python script
        exporter = PythonExporter()
        script, _ = exporter.from_filename(notebook_path)
        with open(temp_script_path, "w", encoding="utf-8") as f:
            f.write(script)
            
        # 2. Load the test suite from test_solutions.py
        suite = unittest.defaultTestLoader.loadTestsFromName('test_solutions')

        # 3. Run the tests with a verbose output
        print(f"--- Running tests for {os.path.basename(notebook_path)} ---\n")
        # Use the default TextTestRunner for detailed, human-readable output
        runner = unittest.TextTestRunner(verbosity=2) 
        result = runner.run(suite)
        print("\n--- Test complete ---")
        
        # This part is for the main autograder script to capture the score
        passed = result.testsRun - len(result.failures) - len(result.errors)
        total = result.testsRun
        # Print a machine-readable summary line at the very end
        print(f"\nSUMMARY_PASSED:{passed}/TOTAL:{total}")

    except FileNotFoundError:
        print(f"ERROR: Notebook file not found at '{notebook_path}'")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)
        
    finally:
        # 4. CRUCIAL: Clean up the temporary files
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)
        if os.path.exists("__pycache__"):
            shutil.rmtree("__pycache__")


if __name__ == '__main__':
    # Check if a command-line argument (the notebook path) was provided
    if len(sys.argv) < 2:
        print("Usage: python run_single_test.py <path_to_notebook.ipynb>")
        sys.exit(1)
    
    notebook_to_grade = sys.argv[1]
    main(notebook_to_grade)