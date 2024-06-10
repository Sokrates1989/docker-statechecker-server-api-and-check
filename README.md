# statechecker-server
Check if your created tools and websites are running correctly and send a telegram message if not.

## Table of contents
1. [Included packages](#included-packages)
2. [Prerequisites](#prerequisites)
   - [Swarm Cronjobs](#swarm-cronjobs)
   - [If on a multiple master swarm](#if-on-a-swarm-cluster-with-multiple-masters)
     - [Option1: Glusterfs or any other distributed, arbitrarily scalable file system like Ceph (recommended)](#option1-glusterfs-or-any-other-distributed-arbitrarily-scalable-file-system-like-ceph-recommended)
     - [Option2: Constrain deployment to a specific node](#option2-constrain-deployment-to-a-specific-node)
   - [Optional: Traefik (recommended)](#optional-traefik-recommended)
3. [First Setup](#first-setup)
   - [Optional: Telegram status messages](#optional-telegram-status-messages)
   - [Optional: Autoscaler State Checker](#optional-autoscaler-state-checker)
4. [Deploy](#deploy)
5. [Usage](#usage)
   - [AutoScaler](#autoscaler)
     - [Quick overview of labels](#autoscaler)
     - [Detailed information of labels](#full-explanation)
     - [Check Logs](#logs)
   - [Grafana](#grafana)
     - [View Autoscaler Metrics](#view-autoscaler-metrics)
     - [Dashboards](#dashboards)


# Included Packages
- statechecker-db 
  - Database to store statecheck items
- statechecker-api
  - An api to allow usage from clients to send alive-messages: https://github.com/Sokrates1989/statechecker-client.git
- statechecker-check 
  - Periodical check of websites, tools and backups


# Prerequisites


# First Setup

### Subdomain

```text
If you want to use the api and phpmyadmin with subdomain in combination with traefik:
Make sure that subdomain exist and points to manager of swarm.
For Example: api.statechecker.domain.de and phpmyadmin.statechecker.domain.de
```


### Setup repo at desired location
```bash
# Choose location on server (glusterfs when using multiple nodes is recommended).
mkdir -p /gluster_storage/swarm/monitoring/statechecker-server
cd /gluster_storage/swarm/monitoring/statechecker-server
git clone https://github.com/Sokrates1989/docker-stateChecker-server.git .
```

### Create secrets in docker swarm

All Secrets must be created for the stack to work. If you are not indending to use a secret, you can just create the secret with the text "none".
```bash
# STATECHECKER DATABASE ROOT PASSWORD.
# This is the password for the root user of the database.
vi secret.txt  # Then insert password (Make sure the token does not contain any backslashes "\") and save the file.
docker secret create STATECHECKER_SERVER_DB_ROOT_USER_PW secret.txt 
rm secret.txt

# STATECHECKER DATABASE USER PASSWORD.
# This is the password for the database user provided in .env used to read and write data.
vi secret.txt  # Then insert password (Make sure the token does not contain any backslashes "\") and save the file.
docker secret create STATECHECKER_SERVER_DB_USER_PW secret.txt 
rm secret.txt

# STATECHECKER GOOGLE DRIVE SERVICE ACCOUNT JSON for google drive backup checks.
# This is the json created during allowing google drive third party applications allow access.
# Insert "none", if you do not want to use google drive backup checks.
vi secret.txt  # Then insert password (Make sure the password does not contain any backslashes "\") and save the file.
docker secret create STATECHECKER_SERVER_GOOGLE_DRIVE_SERVICE_ACCOUNT_JSON secret.txt 
rm secret.txt
```

### Configuration
```bash
# Copy ".env.template" to ".env".
cp .env.template .env

# Edit .env
vi .env
```



# Deploy

#### Requires traefik
```bash
docker stack deploy -c <(docker-compose -f config-stack.yml config) statechecker-server
```