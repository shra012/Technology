FROM quay.io/centos/centos:stream9
LABEL org.opencontainers.image.authors="shravankumar"

RUN dnf update -y && dnf groupinstall -y "Development Tools" \
    && dnf install -y python3 python3-pip hostname wget bind-utils sudo

# Add user ansible in centos
RUN groupadd --gid 1000 ansible \
    && useradd --uid 1000 --gid ansible --shell /bin/bash --create-home ansible \
    && echo "ansible ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible

USER ansible
WORKDIR /home/ansible

RUN pip3 install ansible-navigator ansible-builder
