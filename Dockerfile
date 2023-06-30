FROM python:3.11-alpine

WORKDIR /app

COPY Pipfile Pipfile
COPY Pipfile.lock Pipfile.lock

RUN python3.11 -m venv venv && \
    chmod +x ./venv/bin/activate && \
    ./venv/bin/activate && \
    ./venv/bin/python3 -m pip install pipenv && \
    ./venv/bin/pipenv install
#COPY . .
#CMD [ "python3" , "bot.py"]
