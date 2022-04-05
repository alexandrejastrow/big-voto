FROM node:13-alpine

WORKDIR /src


ENV PATH /src/node_modules/.bin:$PATH

COPY . /src

RUN npm install --silent

RUN npm install react-scripts@3.3.1 -g --silent

CMD ["npm", "start"]