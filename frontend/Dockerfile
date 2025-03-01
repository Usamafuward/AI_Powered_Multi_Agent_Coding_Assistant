FROM python:3.11-slim

WORKDIR /app

# Copy the shared requirements file first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the frontend application and static files
COPY ./frontend /app/frontend
COPY ./static /app/static

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose the port the app runs on
EXPOSE 8010

# Command to run the application
CMD ["uvicorn", "frontend.main:app", "--host", "0.0.0.0", "--port", "8010"]
