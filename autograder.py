import os
import glob
import json
import re
import csv
import sys
import subprocess

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

def main():
    """
    Main function to orchestrate batch grading with sandboxing and timeouts.
    """
    submission_folder = 'submissions'
    notebook_paths = glob.glob(os.path.join(submission_folder, '*.ipynb'))
    results = []
    TIMEOUT_SECONDS = 10  # Set a 10-second limit for each test

    print(f"Found {len(notebook_paths)} notebooks to grade...")

    for path in notebook_paths:
        filename = os.path.basename(path)
        print(f"Grader> Processing: {filename}")

        email = parse_email_from_notebook(path)
        score = "Error"  # Default score

        try:
            # This command runs the grading script inside a secure Docker container
            command = [
                "docker", "run", "--rm",
                "-v", f"{os.getcwd()}:/app", # Mount current directory
                "my-autograder-image",      # The image we built
                "python", "run_single_test.py", path
            ]

            process_result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS  # Apply the timeout here
            )
            
            output = process_result.stdout.strip()
            
            # Find the summary line in the output to get the score
            for line in output.splitlines():
                if line.startswith("SUMMARY_PASSED"):
                    parts = line.split('/')[0].split(':')
                    passed = parts[1]
                    total_parts = line.split('/')[1].split(':')
                    total = total_parts[1]
                    score = f"{passed}/{total}"
                    break
        
        except subprocess.TimeoutExpired:
            # Catch the timeout error and assign a specific score
            print(f"  -> GRADING TIMED OUT for {filename}")
            score = "Timeout Error"
        
        except Exception as e:
            print(f"  -> AN UNEXPECTED ERROR OCCURRED for {filename}: {e}")
            score = "System Error"

        results.append({'email': email, 'score': score, 'file': filename})
        print(f"Grader> Result: {email} -> {score}")

    # Write final results to CSV
    output_file = 'grades.csv'
    with open(output_file, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['email', 'score', 'file'])
        writer.writeheader()
        writer.writerows(results)

    print(f"\nGrading complete. Results saved to {output_file}")


if __name__ == '__main__':
    main()
