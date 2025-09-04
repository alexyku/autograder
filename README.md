# Simple iPython Notebook Autograder

A lightweight, script-based system for automatically grading iPython/Jupyter notebooks (`.ipynb`). This tool converts student notebooks into Python scripts, runs a predefined set of unit tests against the code in an isolated environment, and generates a `grades.csv` report.

---
## How It Works

1.  **Parses Email:** Reads the student's email address from the first markdown cell of the notebook.
2.  **Spawns Secure Container:** Launches a new, isolated **Docker container** for the submission. This acts as a secure sandbox.
3.  **Converts and Tests:** Inside the container, the student's notebook is converted to a Python script and graded against the unit tests from `test_solutions.py`.
4.  **Enforces Timeout:** A strict **timeout limit** is enforced on the container. If the student's code runs for too long (e.g., an infinite loop), the process is automatically terminated.
5.  **Records Result:** The main script captures the test results from the container and adds the score to a final report.
6.  **Generates Report:** After all submissions are processed, it compiles the results into a `grades.csv` file.

---
## Directory Structure

Your project must be organized with the following file structure for the scripts to work correctly:

```
autograder/
├── Dockerfile            # The recipe for the secure sandbox
├── requirements.txt      # Python package dependencies
├── autograder.py         # The main script to run for batch grading
├── test_solutions.py     # Your hidden unit tests
├── run_single_test.py    # Helper script for isolated testing
├── README.md             # This file
└── submissions/
    ├── student1.ipynb
    └── student2.ipynb
```

---
## Prerequisites

The primary prerequisite is **Docker**. The necessary Python packages (like `nbconvert`) are automatically installed inside the Docker environment, so you do not need to install them on your local machine.

* **Docker:** You must have Docker installed and the Docker daemon running. You can download it from the official website: [Docker Desktop](https://www.docker.com/products/docker-desktop/).

---
## Setup & Usage

Follow these steps to set up and run the autograder.

### Step 1: Configure Dependencies
Edit the `requirements.txt` file to list all the Python libraries that students are allowed to use (e.g., `numpy`, `pandas`, `scikit-learn`). The `nbconvert` package, which the autograder needs, should also be in this file.

### Step 2: Write Tests
Define the grading logic and assertions in `test_solutions.py`. Your tests should be written to test functions within a module named `student_code` (e.g., `student_code.my_function()`).

### Step 3: Build the Docker Image (One-Time Setup)
Before you can run the grader, you need to build the Docker image from the `Dockerfile`. This command packages all the necessary tools into a reusable sandbox environment.

**Run this command once from your terminal in the project directory:**
```bash
docker build -t my-autograder-image .
```

### Step 4: Add Student Submissions
Place all student `.ipynb` files into the `submissions/` folder.

### Step 5: Run the Autograder
You can either grade all submissions in a batch or grade a single file for detailed debugging.

**Option A: Batch Grade All Submissions**
To grade every notebook in the `submissions` folder, run the main script:
```bash
python autograder.py
```

**Option B: Grade a Single Submission (for Debugging)**
To get a detailed, real-time report for a specific student, run `run_single_test.py` and pass the path to their notebook:
```bash
python run_single_test.py submissions/student1.ipynb
```

### Step 6: Check Results
After running the batch grader, a `grades.csv` file will be created in the root directory with the email, score, and filename for each submission.

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
