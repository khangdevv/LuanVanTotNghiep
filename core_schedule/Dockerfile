FROM python:3.11-slim

WORKDIR /app

# Copy the pyproject.toml file
COPY pyproject.toml ./

# Install dependencies
RUN pip install --no-cache-dir .

# Copy the rest of the application code
COPY . .

# Expose port 8001 as specified in the architecture document
EXPOSE 8001

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]
