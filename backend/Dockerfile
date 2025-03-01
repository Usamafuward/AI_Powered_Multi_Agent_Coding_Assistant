FROM python:3.11-slim

WORKDIR /app

# Copy the shared requirements file first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the backend application
COPY ./backend /app/backend

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8011

# Command to run the application
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8011"]