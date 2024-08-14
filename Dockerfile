# Use the official Python image as a base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code into the container
COPY ./app /app

# Set MongoDB URL environment variable

ENV MONGODB_URL="mongodb://mongodb:27017/favorites_db"

# Expose the port that FastAPI will run on
EXPOSE 8001

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]

