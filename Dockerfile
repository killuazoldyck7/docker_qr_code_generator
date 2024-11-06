# Use the official Python image from Docker Hub as the base
FROM python:3.12-slim-bullseye

# Set the working directory to /app
WORKDIR /app

# Create a non-root user
RUN useradd -m myuser

# Copy requirements.txt and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories and set permissions
RUN mkdir logs qr_codes && chown myuser:myuser logs qr_codes

# Copy the application code and change ownership to 'myuser'
COPY --chown=myuser:myuser . .

# Switch to non-root user
USER myuser

# Define entrypoint and command
ENTRYPOINT ["python", "main.py"]
CMD ["--url", "https://github.com/killuazoldyck7"]
