FROM node:16.15-slim

WORKDIR /firebase

RUN apt-get update && apt-get install -y curl openjdk-11-jdk

RUN npm install -g firebase-tools

COPY ./config ./config

CMD firebase emulators:start --token $FB_TOKEN -c config/firebase.json
