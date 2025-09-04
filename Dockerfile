# Use a lightweight, official Python image as the base
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy your autograder scripts into the container
# We only need the files the container will run
COPY test_solutions.py ./
COPY run_single_test.py ./

# Copy the requirements file into the container
COPY requirements.txt .

# Install the necessary Python packages
RUN pip install -r requirements.txt

# By default, Docker runs as root. For better security,
# create a non-priveleged user and switch to it.
RUN useradd --create-home student
USER student
