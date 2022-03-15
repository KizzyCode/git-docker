FROM alpine:latest

RUN apk add --no-cache git openssh python3 shadow
COPY ./files/ssh* /etc/ssh/
COPY ./files/git* /usr/libexec/

EXPOSE 80
CMD ["/usr/libexec/git-service.py"]
