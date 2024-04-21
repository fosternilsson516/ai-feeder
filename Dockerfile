FROM python:alpine3.19
WORKDIR /app

# Copy your Python script and other necessary files
COPY . /app

COPY cli_tool.py /app/
COPY output/ /app/

# Install any required dependencies
RUN pip install pandas matplotlib

# Expose the port the server will listen on
EXPOSE 8000

# Run the Python script
ENTRYPOINT ["python3", "cli_tool.py"]
