# 1. Using official Python runtime as a parent image
FROM python:3.10-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        default-libmysqlclient-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 4. Create a working directory
WORKDIR /app

# 5. Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy entire project into the container
COPY . /app/

# 7. Create a non-root user for security
RUN adduser --disabled-password --no-create-home appuser
USER appuser

# 8. Expose port 8000 for Django
EXPOSE 8000

# 9. Default command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
