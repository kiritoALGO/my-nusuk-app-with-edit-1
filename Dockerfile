# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y libfreetype6-dev libharfbuzz-dev libfribidi-dev && \
    apt-get clean

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /usr/src/app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . /usr/src/app/

# Install libraqm and Pillow
RUN pip install libraqm pillow

# Expose the port on which Django runs
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
