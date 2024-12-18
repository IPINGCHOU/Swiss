# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory
WORKDIR /app

# Install basic dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl

# Install and configure poetry
RUN pip install --no-cache-dir poetry==1.7.1
RUN poetry config virtualenvs.in-project false

# Copy project files
COPY . .

# Install dependencies
RUN poetry install --only main --no-interaction --no-ansi

# Expose port 80
EXPOSE 80

# Command to run streamlit directly on port 80
CMD ["poetry", "run", "streamlit", "run", "app/main.py", "--server.port", "80"]
