
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /

# Install dependencies.
RUN pip install -r /requirements.txt

# Set work directory.
RUN mkdir /app
WORKDIR /app

# Copy project code.
COPY . /app/

RUN python manage.py makemigrations

EXPOSE 8000