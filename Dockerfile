FROM python:alpine3.19
WORKDIR /app

# Copy your Python script and other necessary files
COPY . /app

# Install any required dependencies
RUN pip install pandas matplotlib

# Expose the port the server will listen on
EXPOSE 8000

# Run the Python script
CMD ["python", "cli_tool.py"]
