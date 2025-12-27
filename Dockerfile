# Use the official Python 3.9 image with latest security updates
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code
COPY . /app

# Start the bot.
CMD ["python", "bot.py"]