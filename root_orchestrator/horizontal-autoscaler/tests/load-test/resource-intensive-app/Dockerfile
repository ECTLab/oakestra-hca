FROM golang:1.19-alpine as build

WORKDIR /src

COPY main.go /src

RUN go build main.go

FROM --platform=linux/amd64 alpine as runtime

COPY --from=build /src/main /app/main

CMD [ "/app/main" ]