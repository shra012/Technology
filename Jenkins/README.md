# Jenkins with artifactory-oss backed by postgressql and sonarqube backed by elastic search.

This repository brings up a Jenkins with a agent, artifactory-oss backed by postgressql and sonarqube backed by elastic search.

## Things to Configure,

For setting up the artifactory-oss and postgres we have to edit the .artifactory/etc/system.yaml

```yaml
## Database Configuration
database:
  ## One of mysql, oracle, mssql, postgresql, mariadb
  ## Default Embedded derby

  ## Example for postgresql
  type: postgresql
  driver: org.postgresql.Driver
  url: 'jdbc:postgresql://postgresql-fs:5432/artifactory'
  username: artifactory
  password: password
```

For setting up the jenkins agent please refer setting up a agent [post](https://www.cloudbees.com/blog/how-to-install-and-run-jenkins-with-docker-compose)
