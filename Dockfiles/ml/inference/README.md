# Inference Container

## Introduction

This container acts as a service for inference on ML models. 

## Building the container

```
docker build --tag epython-ml-inference:1.0 .
```

## Testing Locally

### Run FastAPI Directly

```
uvicorn main:app --host 0.0.0.0 --port 8080
```


### Run in Container under ECS environment

```
docker-compose up
```

More details here: https://aws.amazon.com/blogs/compute/a-guide-to-locally-testing-containers-with-amazon-ecs-local-endpoints-and-docker-compose/

Now point browser at http://[::1]:8080/docs

Notice WSL2 binds localhost on IPV6 address.

### Test Data

One can use the data in test_marketdata.json for testing.
