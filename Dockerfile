FROM python:3.11-slim

WORKDIR /code

# Upgrade pip and install build tools
RUN pip install --upgrade pip setuptools wheel

# Copy and install requirements (using pre-built wheels when possible)
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r /code/requirements.txt

# Copy application code
COPY ./app /code/app

# Expose port
EXPOSE 80

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]