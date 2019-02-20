FROM python:3.7.2 AS base
ARG PROJECT=project

WORKDIR /tmp/
RUN apt-get update \
    && apt-get install -y --no-install-recommends libhdf5-dev \
    && rm -rf /var/lib/apt/lists/*

FROM base AS build
ARG PROJECT=project
ARG SSH_PRIVATE_KEY

WORKDIR /usr/src/${PROJECT}

RUN mkdir /root/.ssh/
RUN printf -- "${SSH_PRIVATE_KEY}" >> /root/.ssh/id_rsa && chmod 600 /root/.ssh/id_rsa
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

COPY requirements.txt requirements-dev.txt requirements-test.txt ./
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r requirements-dev.txt \
    && pip install --no-cache-dir -r requirements-test.txt

FROM base
ARG PROJECT=project

COPY --from=build /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
COPY --from=build /usr/local/bin/flake8 /usr/local/bin/mypy /usr/local/bin/

WORKDIR /usr/src/${PROJECT}

COPY . ./

RUN pip install --no-cache-dir .

ENTRYPOINT [ "/bin/bash", "-c" ]
