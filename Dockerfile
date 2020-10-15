FROM python:3.8.2
WORKDIR /code

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /code/
RUN pipenv install --system

# Copy project
COPY docker-entrypoint.sh /code/
RUN chmod +x docker-entrypoint.sh

COPY . /code/

CMD ./docker-entrypoint.sh

