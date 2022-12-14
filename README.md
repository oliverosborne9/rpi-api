[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=oliverosborne9_rpi_api&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=oliverosborne9_rpi_api)
[![Maintainability Rating](https://sonarcloud.io/api/project_badges/measure?project=oliverosborne9_rpi_api&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=oliverosborne9_rpi_api)
[![Reliability Rating](https://sonarcloud.io/api/project_badges/measure?project=oliverosborne9_rpi_api&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=oliverosborne9_rpi_api)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/oliverosborne9/rpi-api/main.svg)](https://results.pre-commit.ci/latest/github/oliverosborne9/rpi-api/main)


# mechanic

Device module (Python package and Docker container) with HTTP API for reading from electronic scales and controlling servo motors. Designed for Raspberry Pi, running a Debian-based distribution.

## API Documentation

Documentation for the RPi mechanic module can be found [here](https://oliverosborne9.github.io/rpi-api/).


## Setup

First, run the following command natively on the shell of your Raspberry Pi:
`sudo systemctl enable pigpiod`
This is required for controlling the GPIO pins and therefore controlling the attached servo motors.


## Usage

`mechanic`

Once this package has been installed, launch the API with the command `mechanic`.

`docker compose up --build`

Alternatively, opt for running the module in a Docker environment. The Docker Compose YAML file provided also includes the default Redis container, which acts as a backend and broker for the Celery tasks (dispensing).
