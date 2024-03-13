# Ansible Ecosystem
Projects in the Ansible ecosystem let you expand automation to a virtually unlimited set of use cases. Click [here](https://docs.ansible.com/ecosystem.html) to learn more.

## Set up
- Copy your public key into `ssh/authorized_hosts` and your private key into `ssh/rsa`. Click [here](https://www.ssh.com/academy/ssh/keygen#creating-an-ssh-key-pair-for-user-authentication) for steps to create a new ssh key pair
- Add your public key to the `ansible-worker1`'s -> `environment` -> `PUBLIC_KEY` in the `docker-compose.yml`