FROM lscr.io/linuxserver/openssh-server:latest
LABEL org.opencontainers.image.authors="shravankumar"

RUN apk add --update python3 py3-pip wget doas bash

# Add user ansible in centos
RUN addgroup --gid 1008 ansible \
    && useradd --uid 1008 --gid ansible --shell /bin/bash --create-home ansible \
    && echo 'permit baeldung as root' > /etc/doas.d/doas.conf

USER ansible
WORKDIR /home/ansible