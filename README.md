# Sending simulated Floating Car Data to a TCP socket

This python script generates Floating Car Data (FCD) and send them to a given HOST and PORT as TCP packages.

## Installation

```
pip install fcdsim
```

## Usage

```
usage: fcdsim [-h] [-r NUM_REQUESTS] [-f NUM_FAULTY] HOST PORT

positional arguments:
  HOST                  Host to send the simulated Floating Car Data to
  PORT                  TCP port to send the simulated Floating Car Data to

optional arguments:
  -h, --help            show this help message and exit
  -r NUM_REQUESTS, --requests-per-second NUM_REQUESTS
                        The overall number of requests per second to send to
                        the host. Default: 100
  -f NUM_FAULTY, --faulty-data-per-second NUM_FAULTY
                        The number of requests per second, which contains
                        faulty Floating Car Data. This is limited by the
                        overall number of requests allowed. Default: 10
```
