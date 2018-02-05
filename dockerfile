FROM alpine:3.6
MAINTAINER james collins
RUN   apk add curl python3 python3-dev jpeg-dev bash  make g++ zlib-dev git gcc postgresql-dev --no-cache  --repository http://dl-cdn.alpinelinux.org/alpine/edge/main/
RUN curl https://bootstrap.pypa.io/get-pip.py | python3
RUN mkdir api
WORKDIR api
COPY . api
RUN  pip3 install requirements
EXPOSE 8080
CMD python3 manage.py db init\
    python3 manage.py db migrate\
    python3 manage.py db upgrade\
    python3 run.py