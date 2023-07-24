FROM node:18-alpine

WORKDIR /app

RUN apk add --no-cache curl

COPY . .

RUN npm install

CMD [ "npm", "run", "start" ]
