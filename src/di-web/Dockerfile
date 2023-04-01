# Phase 1: Use node.js image to build front-end static files
FROM node:18-alpine AS build

WORKDIR /src/di-web

COPY package.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn build

# Phase 2: Use Nginx image as the base image and copy the built static files from the first phase
FROM nginx:stable

COPY --from=build /src/di-web/build /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf