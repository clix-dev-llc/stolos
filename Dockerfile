FROM python:2.7.11
MAINTAINER Antonis Kalipetis <akalipetis@sourcelair.com>

# Install system dependencies
RUN apt-get update &&\
    apt-get install -y netcat && \
    mkdir -p /usr/src/app && \
    rm -rf /var/lib/apt/lists/*
WORKDIR /usr/src/app

# Set the entrypoint
COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]

# Install Python requirements
COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

# Add static assets - the assets should have been built already
COPY dashboard/static/dashboard /usr/src/app/dashboard/static/dashboard

# Add the rest of the code
COPY . /usr/src/app

CMD ["make", "prod"]
