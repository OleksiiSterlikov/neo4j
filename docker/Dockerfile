# Python official runtime image
FROM python:3.12

# Set environment variables
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Create the app directoty
RUN mkdir /app

# Set the working directory
WORKDIR /app

# Add all files project directory to the working directory
ADD . /app

# Run command to install all dependencys and upgrade packages
RUN pip install --upgrade pip # && pip install -r requirements.txt

RUN neo4j
# Copy Project to the container
COPY . /app
