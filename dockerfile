# Use an ARM64-based image to match the Raspberry Pi
FROM arm64v8/python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file first to leverage Docker's build cache
COPY requirements.txt .

# Run pip install to install all dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Now copy the rest of your project code
COPY . .

# Define the default command (e.g., start a shell for development)
CMD ["python", "src/main.py"]