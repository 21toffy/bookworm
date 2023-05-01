FROM python:3.8-slim-buster


RUN apt-get update && apt-get install -y mongo-tools



# setting work directory
WORKDIR /usr/src/app


# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1



# install dependencies

RUN pip install --upgrade pip
COPY ./requirements.txt ./
COPY ./.env ./
RUN pip install -r requirements.txt

# COPY ./entrypoint /.
# RUN chmod +x /entrypoint

COPY . .
# ENTRYPOINT [ "/entrypoint" ]