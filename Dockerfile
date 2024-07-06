FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY /Pipfile.lock /Pipfile /app/
RUN pip install pipenv && pipenv install --system --dev --ignore-pipfile
COPY . /app

CMD ["gunicorn", "-c", "gunicorn.conf.py", "--bind", ":8000", "config.wsgi:application", "--reload"]
