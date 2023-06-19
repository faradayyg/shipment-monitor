# Shipment
This document describes the setup on an up to date macOS machine. If you need to work on a non-mac machine, please keep in mind that you'll need to adapt things to suit your needs in places.
I reckon this should work as-is on a Linux machine.


## Prerequisites
- Make *
- Poetry *
- A Redis server *
- A Postgres DB *
- Docker
- Python > 3.10 (use pyenv for easy version management)


> 💡
> Requirements marked with `*` are only necessary for bare machine setup (Setup without docker)

## Setup

To set up this project, copy the `.env.template` file to `.env` and fill it up with the proper configuration data of your local environment.

### Developing directly on your machine

- Clone this repository
- [Install poetry](https://python-poetry.org/docs/) or `pip install poetry`
- Copy the `.env.template` to `.env`
- Adjust the `.env` file, fill in the variables with the correct values
- Run the initial setup: `make setup` (This also seeds the data)
- Run the project: `make run`

### Using Docker

If you wish to use docker for development, do the following:
- Install docker desktop
- Copy the `.env.template` to `.env`
- Run `docker compose up` to bring the project up.

The application is available at http://127.0.0.1:8000

There is a redoc OpenAPI documentation available at http://127.0.0.1:8000/redoc
Swagger UI is also available at http://127.0.0.1:8000/swagger


## Running Tests
 - `make test`
