# syntax=docker/dockerfile:experimental
FROM python:2.7-stretch

LABEL name=bluebottle \
      version=0.1 \
      maintainer="info@viperdev.io"

#CMD ["docker/run.sh"]

EXPOSE 8080

HEALTHCHECK \
    CMD curl --fail http://127.0.0.1:8080/ || exit 1

ENV BLUEBOTTLE_ROOT=/opt/bluebottle \
    BLUEBOTTLE_USER=cookie \
    LOG_LEVEL=info


WORKDIR $BLUEBOTTLE_ROOT

RUN useradd -d $BLUEBOTTLE_ROOT -r $BLUEBOTTLE_USER

RUN --mount=type=cache,target=/var/cache/apt --mount=type=cache,target=/var/lib/apt \
    rm -f /etc/apt/apt.conf.d/docker-clean; echo 'Binary::apt::APT::Keep-Downloaded-Packages "true";' > /etc/apt/apt.conf.d/keep-cache && \
    apt-get update && \
    apt-get install --no-install-recommends -y \
        gdal-bin \
        gettext \
        libcairo2 \
        libgdk-pixbuf2.0-0 \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libsqlite3-mod-spatialite \
        libxmlsec1-dev \
        libyaml-dev \
        postgresql-client \
        && \
    apt-get clean

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip

# requirements.txt created with
# $  dephell deps convert --from-path setup.py --from-format=setuppy \
#                         --to-path requirements.txt --to-format=pip

ADD requirements.txt $BLUEBOTTLE_ROOT

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -rrequirements.txt

ADD . $BLUEBOTTLE_ROOT

#RUN --mount=type=cache,target=/root/.cache/pip \
#    python setup.py install

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install .

RUN pip freeze > requirements.freeze

RUN cat requirements.freeze

RUN mkdir $BLUEBOTTLE_ROOT/tenants
 
RUN python manage.py collectstatic --no-input

RUN python manage.py migrate_schemas --help

RUN echo "SECRET_KEY = 'secret key'" >> bluebottle/settings/secrets.py
