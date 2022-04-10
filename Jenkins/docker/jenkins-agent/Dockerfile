FROM jenkins/ssh-agent:latest

WORKDIR /home/jenkins

RUN apt-get update && apt-get install ca-certificates maven python3 -y

ENTRYPOINT [ "setup-sshd" ]
