# mechanic

Device module (Python package and Docker container) with HTTP API for reading from electronic scales and controlling servo motors. Designed for Raspberry Pi, running a Debian-based distribution.

## Setup

First, run the following command natively on the shell of your Raspberry Pi:
`sudo systemctl enable pigpiod`
This is required for controlling the GPIO pins and therefore controlling the attached servo motors.


## Usage

`mechanic`

Once this package has been installed, launch the API with the command `mechanic`.

`docker compose up --build`

Alternatively, opt for running the module in a Docker environment. The Docker Compose YAML file provided also includes the default Redis container, which acts as a backend and broker for the Celery tasks (dispensing).
