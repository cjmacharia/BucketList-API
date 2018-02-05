FROM alpine:3.6
MAINTAINER james collins
RUN   apk add curl python3 python3-dev linux-headers musl-dev python-dev build-base openssl libffi-dev jpeg-dev bash libffi make g++ zlib-dev git gcc postgresql-dev --no-cache
COPY . BucketList-API
WORKDIR BucketList-API
RUN  pip3 install -r requirements.txt
EXPOSE 8080
CMD python3 manage.py db init\
    python3 manage.py db migrate\
    python3 manage.py db upgrade\
    python3 run.py