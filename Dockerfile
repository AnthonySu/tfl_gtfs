FROM debian:wheezy
MAINTAINER Gerry Casey <gac55@cam.ac.uk>

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/hello-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/hello-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Update apt-get
RUN apt-get update

# Get what I need
RUN apt-get install -y python-pip
# RUN apt-get install -y python-pip python-dev build-essential 
RUN apt-get install -y git
RUN apt-get install -y nano
RUN export EDITOR="/usr/bin/nano"
RUN apt-get install -y cron
RUN apt-get install -y mailutils
RUN apt-get install -y ssmtp

# Python dependencies
RUN pip install awscli
# RUN pip install ujson
RUN pip install requests
RUN pip install python-dateutil
RUN pip install boto
RUN pip install magicdate
RUN pip install filechunkio

# needed by cargo
ENV USER root

ADD install.sh install.sh
RUN chmod +x install.sh && ./install.sh && rm install.sh

WORKDIR /home

COPY . tflgtfs

WORKDIR tflgtfs

# AWS S3 credential setup
RUN cat mail > /etc/ssmtp/ssmtp.conf
RUN mkdir /root/.aws/
RUN mv config  /root/.aws/
RUN mv credentials  /root/.aws/
ENV AWS_ACCESS_KEY_ID="TODO"
ENV AWS_SECRET_ACCESS_KEY="TODO"
ENV HOME=/root

ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt

RUN cargo build --release --verbose 

VOLUME ["/source"]
WORKDIR /source

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log

WORKDIR /home/tflgtfs

