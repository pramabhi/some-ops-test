FROM python:3.7-stretch

# Create a working directory.
RUN mkdir /app
WORKDIR /app

# Copy the code
COPY . ./

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 gunicorn_app
