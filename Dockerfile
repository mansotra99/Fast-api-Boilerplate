FROM python:3.8.12-slim

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /code/
# Install dependencies
RUN pip install pipenv
RUN pipenv install 
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system --dev
COPY . /code/


CMD ["python","main.py"]
