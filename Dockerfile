# Use the latest Python base image
FROM python:latest

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script into the container
COPY main.py .

# Run the bot script
CMD ["python", "main.py"]
