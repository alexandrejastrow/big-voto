FROM golang:1.18-alpine AS build

WORKDIR /app

COPY . /app

RUN go mod download

RUN go build -o /voteService

CMD [ "/voteService" ]