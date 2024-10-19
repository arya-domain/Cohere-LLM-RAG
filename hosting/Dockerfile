# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /workspaces/Cohere-LLM-RAG-/hosting

# Copy the requirements.txt file into the container at the working directory
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir --root-user-action=ignore --disable-pip-version-check -r requirements.txt

# Copy the rest of the application code to the working directory
COPY . .

# Expose port 7860 to be accessible from the host machine
EXPOSE 7860

# Set environment variable for Gradio to bind to all available IP addresses
ENV GRADIO_SERVER_NAME="0.0.0.0"

# Run main.py when the container launches
CMD ["python", "main.py"]
