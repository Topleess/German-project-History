FROM node:18-alpine

WORKDIR /app

COPY package*.json ./

RUN npm install --no-optional

COPY . .

RUN npm run generate

ENV HOST=0.0.0.0
ENV PORT=3000

EXPOSE 3000

RUN npm install -g http-server
CMD ["http-server", "./.output/public", "-p", "3000"] 