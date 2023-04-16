FROM python:3.8

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt


COPY . /app/

# Run the Django application with Daphne
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "config.asgi:application"]