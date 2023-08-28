# FINAL #

# pull official base image
FROM python:3.11.5-alpine3.17

# create directory for the app user
RUN mkdir -p /home/app

# create the app user
RUN addgroup -S app && adduser -S app -G app

# create the appropriate directories
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/static
WORKDIR $APP_HOME

# install dependencies
RUN apt-get update && apt-get install -y libpq-dev
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint-prod.sh
COPY ./config/docker/entrypoint.prod.sh $APP_HOME/config/docker/entrypoint.prod.sh

# copy project
COPY . $APP_HOME

# chown all the files to the app user
RUN chown -R app:app $APP_HOME

# change to the app user
USER app
