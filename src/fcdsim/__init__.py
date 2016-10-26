import argparse

arg_parser = argparse.ArgumentParser(prog=u'fcdsim')
arg_parser.add_argument('host',
                        metavar='HOST',
                        help='Host to send the simulated Floating Car Data to')
arg_parser.add_argument('port',
                        metavar='PORT',
                        type=int,
                        help='TCP port to send the simulated Floating Car Data to')
arg_parser.add_argument('-r', '--requests-per-second',
                        type=int,
                        default=100,
                        metavar='NUM_REQUESTS',
                        help='The overall number of requests per second to send to the host. Default: 100')
arg_parser.add_argument('-f', '--faulty-data-per-second',
                        type=int,
                        default=10,
                        metavar='NUM_FAULTY',
                        help='The number of requests per second, which contains faulty Floating Car Data. This is \
                        limited by the overall number of requests allowed. Default: 10')


def __main__():
    args = arg_parser.parse_args()
    # TODO

