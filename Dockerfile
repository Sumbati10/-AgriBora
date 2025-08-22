# Use a stable Python runtime
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy dependencies first (better caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . /app

# Expose port 5000
EXPOSE 5000

# Environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Use Gunicorn (better than flask run in production)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
