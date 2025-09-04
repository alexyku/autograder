import os
import glob
import json
import re
import csv
import unittest
import sys
from nbconvert import PythonExporter

def parse_email_from_notebook(notebook_path):
    """
    Parses the email address from the first markdown cell of a notebook.
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook_content = json.load(f)

    for cell in notebook_content['cells']:
        if cell['cell_type'] == 'markdown':
            # Join the source lines and search for the email pattern
            source_text = "".join(cell['source'])
            # A robust regex for finding emails
            match = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', source_text)
            if match:
                return match.group(0) # Return the first email found
    return "email_not_found"

def grade_submission(notebook_path, test_module_name):
    """
    Converts, imports, and tests a single student notebook.
    Returns the number of tests passed and the total number of tests.
    """
    # This is the known name our test file will import
    temp_script_path = "student_code.py"
    
    # Ensure no old versions are lingering before we start
    if "student_code" in sys.modules:
        del sys.modules["student_code"]

    try:
        # 1. Convert notebook to a Python script
        exporter = PythonExporter()
        script, _ = exporter.from_filename(notebook_path)

        # 2. Write the script to our temporary file
        with open(temp_script_path, "w", encoding="utf-8") as f:
            f.write(script)

        # 3. Run unit tests
        suite = unittest.defaultTestLoader.loadTestsFromName(test_module_name)
        # Suppress test output to the console for a cleaner grading summary
        runner = unittest.TextTestRunner(stream=open(os.devnull, 'w'))
        result = runner.run(suite)
        
        passed = result.testsRun - len(result.failures) - len(result.errors)
        total = result.testsRun
        return passed, total

    finally:
        # 4. CRUCIAL CLEANUP STEP
        # This block runs whether the tests succeeded or failed.
        
        # Remove BOTH the student's code AND the test module from Python's cache.
        # This is the key to preventing state leakage between runs.
        if "student_code" in sys.modules:
            del sys.modules["student_code"]
        if "test_solutions" in sys.modules:
            del sys.modules["test_solutions"]

        # Delete the temporary python script
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)
        
        # Delete the __pycache__ folder that Python creates
        if os.path.exists("__pycache__"):
            import shutil
            shutil.rmtree("__pycache__")

def main():
    """
    Main function to orchestrate the grading process.
    """
    submission_folder = 'submissions'
    notebook_paths = glob.glob(os.path.join(submission_folder, '*.ipynb'))
    results = []

    print(f"Found {len(notebook_paths)} notebooks to grade...")

    for path in notebook_paths:
        filename = os.path.basename(path)
        print(f"Grader> Processing: {filename}")

        # Get student email
        email = parse_email_from_notebook(path)

        # Grade the notebook
        passed, total = grade_submission(path, 'test_solutions')
        score = f"{passed}/{total}"

        results.append({'email': email, 'score': score, 'file': filename})
        print(f"Grader> Result: {email} -> {score}")

    # Write results to a CSV file
    output_file = 'grades.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['email', 'score', 'file'])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nGrading complete. Results saved to {output_file}")


if __name__ == '__main__':
    main()
