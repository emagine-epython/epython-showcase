# Dash Demo

## Introduction

This is a container to run ePython dash demo


## Testing Locally

### Run dash in gunicorn

```
gunicorn --workers 2 app:server
```

### Run in Container under ECS environment

Dependency library

```
cp -rf ../../tsdb/ .
```

Start docke-compose

```
docker-compose up
```

More details here: https://aws.amazon.com/blogs/compute/a-guide-to-locally-testing-containers-with-amazon-ecs-local-endpoints-and-docker-compose/

Now point browser at http://[::1]:8080/docs

Notice WSL2 binds localhost on IPV6 address.
