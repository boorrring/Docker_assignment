FROM node:16-alpine

ENV BACKEND_URL = http://localhost:5001

ADD . /app

WORKDIR /app

RUN npm install

ENTRYPOINT ["npm"]

CMD ["start"]