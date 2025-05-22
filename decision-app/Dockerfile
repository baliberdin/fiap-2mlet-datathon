FROM node:23.11.1-alpine

WORKDIR /opt/decision_app

COPY ./bin ./bin
COPY ./public ./public
COPY ./routes ./routes
COPY ./views ./views
COPY app.js .
COPY package.json .
COPY package-lock.json .

# Custom folders
COPY ./api ./api
COPY ./services ./services
COPY ./db ./db

RUN npm install

CMD ["npm", "start"]