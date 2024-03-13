FROM quay.io/centos/centos:stream9
LABEL org.opencontainers.image.authors="shravankumar"


RUN dnf update -y && dnf groupinstall -y "Development Tools"

RUN dnf install -y python3 python3-pip hostname wget bind-utils  \
    && pip3 install ansible-navigator ansible-builder