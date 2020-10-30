FROM python:3.8.2

RUN mkdir /backend
WORKDIR /backend
RUN mkdir /backend/static

# Install dependencies
RUN pip install pipenv
COPY Pipfile Pipfile.lock /backend/
RUN pipenv install --system
# Copy project
COPY docker-entrypoint.sh /backend/
RUN chmod +x docker-entrypoint.sh

COPY . /backend/

CMD ./docker-entrypoint.sh
