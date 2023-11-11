FROM node:21-alpine3.18

WORKDIR /app

COPY package.json package.json

RUN npm install && npm install -g serve

COPY . .

RUN npm run build

CMD ["serve", "-s", "build", "-l", "8001"]
