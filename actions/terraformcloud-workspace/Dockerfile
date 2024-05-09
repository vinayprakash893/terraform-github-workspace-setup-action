FROM python:3.10-alpine

WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org

COPY main.py /app/main.py
COPY entrypoint.py /app/entrypoint.py

RUN chmod +x /app/entrypoint.py

CMD ["python3", "/app/entrypoint.py"]
