FROM python:3.13.2

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY ../../documentacao/requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Start the application
CMD ["python", "cliente/app.py"]