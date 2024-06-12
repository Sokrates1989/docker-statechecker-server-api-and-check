# statechecker-server-api-and-check
Combined repo for both statechecker-server-check and statechecker-server-api-and-check

To deploy use https://github.com/Sokrates1989/swarm-statechecker-server.git

# Backlog
Stuff to do, that just could not be done in time
- Server auth token
- Logging
    - Log and print via telegram and email as well
    - Log more
- print every: customize in settings and allow disabling
- google drive folders as secret json instead of .env statechecker config json


# Push API to dockerhub

```bash
docker image ls sokrates1989/statechecker-server-api-and-check
```

```bash
docker build -t statechecker-server-api-and-check .
docker tag statechecker-server-api-and-check sokrates1989/statechecker-server-api-and-check:latest
docker tag statechecker-server-api-and-check sokrates1989/statechecker-server-api-and-check:major.minor.patch
docker login
docker push sokrates1989/statechecker-server-api-and-check:latest
docker push sokrates1989/statechecker-server-api-and-check:major.minor.patch
```


## Debug images

### Create

```bash
docker build -t statechecker-server-api-and-check .
docker tag statechecker-server-api-and-check sokrates1989/statechecker-server-api-and-check:DEBUG-major.minor.patch
docker login
docker push sokrates1989/statechecker-server-api-and-check:DEBUG-major.minor.patch
docker image ls sokrates1989/statechecker-server-api-and-check
git status

```
### Cleanup / Delete
```bash
docker rmi sokrates1989/statechecker-server-api-and-check:DEBUG-major.minor.patch
```

