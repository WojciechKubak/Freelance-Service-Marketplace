FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY /Pipfile.lock /Pipfile /app/
RUN pip install pipenv && pipenv install --system --dev --ignore-pipfile
COPY . /app
