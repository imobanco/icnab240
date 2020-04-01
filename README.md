# pyCNAB240


## Docker + docker-compose

Install [docker-ce](https://docs.docker.com/install/) and 
[docker-compose](https://docs.docker.com/compose/install/) from each documentation.


### Running using Docker (development):

First build a image named `cnab`.

`docker build --tag cnab .`

Running in development:
```
docker run -it \
--rm \
--env-file .env \
--volume "$(pwd)":/code \
--workdir /code \
cnab \
bash
```

### Running using Docker Compose (development):

First build:

`docker-compose build`

For development use: 

`docker-compose run cnab bash`

Note: the above command uses `run`, for development it is really handy.
