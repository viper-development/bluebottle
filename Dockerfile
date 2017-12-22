# TODO: Create a local user, dont't use root
# TODO: Do not copy SQL into docker image
# TODO: Setup postgres credentials via env file
FROM python:2.7.14-alpine3.7

#The ARG instruction defines a variable that users can pass at build-time to the builder with the docker build
# command using the --build-arg <varname>=<value> flag.
#The ENV instruction sets the environment variable <key> to the value <value>.
#The environment variables set using ENV will persist when a container is run from the resulting image.
# git log -1 --format="%H"
ARG GIT_COMMIT=unknown

# Use label schema to annotate the Dockerfile (http://label-schema.org/rc1/)
LABEL org.label-schema.schema-version="1.0.0-rc.1" \
      org.label-schema.name="bluebottle" \
      org.label-schema.description="Social do-good platform" \
      org.label-schema.vcs-url="https://github.com/onepercentclub/bluebottle" \
      org.label-schema.version="1.2.3" \
      org.label-schema.vcs-ref=$GIT_COMMIT \
      org.label-schema.build-date="2017-07-01T00:00:00.00Z" \
      org.label-schema.vendor="1%Club" \
      org.label-schema.url="http://www.onepercentclub.com" \
      org.label-schema.usage="N/A e.g.:/usr/doc/app-usage.txt" \
      org.label-schema.docker.cmd="docker run -d -p 8000:8000 -v config.json:/etc/config.json myapp" \
      org.label-schema.docker.cmd.devel="docker run -d -p 8000:8000 -e ENV=DEV myapp" \
      org.label-schema.docker.cmd.test="docker run bluebottle" \
      org.label-schema.docker.debug="docker exec -it bluebottle /bin/bash" \
      org.label-schema.docker.cmd.help="docker exec -it bluebottle /bin/bash --help" \
      org.label-schema.docker.params="NO_THREADS=integer number of threads to launch"

RUN apk add --update \
    python \
    python-dev \
    mercurial \
    git \
    py-pip \
    postgresql-dev \
    libxml2-dev \
    xmlsec-dev \
    jpeg-dev \
    build-base \
  && rm -rf /var/cache/apk/*

ENV LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

WORKDIR /app

COPY . /app
RUN pip install -e .[dev,test] --process-dependency-links --trusted-host github.com

EXPOSE 8000

#RUN chmod +x /app/docker-entrypoint.sh
ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["./run-api.sh"]
