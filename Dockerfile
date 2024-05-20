# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# If you have a MongoDB connection string, you can set it as an environment variable
ENV MONGO_URI="mongodb+srv://s26670:3vpHvtdXyLuk1oBE@cluster0.xhxbyrd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Run the Flask app
CMD ["flask", "run"]