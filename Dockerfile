# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
# (Skip this if you don't have a requirements.txt, or you can add it later if needed)
RUN pip install --no-cache-dir -r requirements.txt || true

# Expose any port the app runs on, if applicable (e.g., 8000)
EXPOSE 8000

# Run the app
CMD ["python", "app.py"]
