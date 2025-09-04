# Simple iPython Notebook Autograder

A lightweight, script-based system for automatically grading iPython/Jupyter notebooks (`.ipynb`). This tool converts student notebooks into Python scripts, runs a predefined set of unit tests against the code in an isolated environment, and generates a `grades.csv` report.

---
## How It Works

The main `autograder.py` script iterates through each notebook in the `submissions/` directory and performs the following steps for each:
1.  **Parses Email:** Reads the student's email address from the first markdown cell.
2.  **Converts Notebook:** Transforms the `.ipynb` file into a temporary `student_code.py` script.
3.  **Tests in Isolation:** Spawns a separate subprocess to run the unit tests from `test_solutions.py` against the student's code. This ensures that each student's submission is graded in a clean, isolated environment, preventing errors or state from one submission from affecting another.
4.  **Records Result:** Captures the test results (e.g., "3/3 passed") from the subprocess.
5.  **Generates Report:** After processing all notebooks, it compiles the results into a `grades.csv` file.

---
## Directory Structure

Your project must be organized with the following file structure for the scripts to work correctly:

```
autograder/
├── autograder.py         # The main script to run
├── test_solutions.py     # Your hidden unit tests
├── run_single_test.py    # Helper script for isolated testing
├── README.md             # This file
└── submissions/
    ├── student1.ipynb
    └── student2.ipynb
```

---
## Prerequisites

The only external library required is `nbconvert`.

```bash
pip install nbconvert
```

---
## Usage

1.  **Write Tests:** Define the grading logic and assertions in `test_solutions.py`. Your tests should be written to test functions within a module named `student_code` (e.g., `student_code.my_function()`).

2.  **Add Submissions:** Place all student `.ipynb` files into the `submissions/` folder.

3.  **Run the Autograder:** Execute the main script from your terminal.
    ```bash
    python autograder.py
    ```
4.  **Check Results:** A `grades.csv` file will be created in the root directory with the email, score, and filename for each submission.

---
## Instructions for Students

For the autograder to work, students must follow two simple rules:

1.  **Provide Your Email:** You must include your email address in the **first markdown cell** of your notebook. The script will parse this cell to identify you.

    *Example Markdown Cell:*
    ```markdown
    # Problem Set 1
    **Name:** Jane Doe
    **Email:** jane.doe@university.edu
    ```

2.  **Use Correct Function Names:** Your functions must be named exactly as specified in the problem set instructions (e.g., `add_numbers`, `calculate_average`, etc.) so the unit tests can find them.
