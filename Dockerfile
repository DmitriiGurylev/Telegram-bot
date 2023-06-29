FROM python:3.11-alpine

WORKDIR /app
COPY Pipfile.lock Pipfile.lock
RUN pip3 install --upgrade pipenv && pipenv install
COPY . .
CMD [ "python3" , "bot.py"]