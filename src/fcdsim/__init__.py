import argparse
import random
import socket
from sys import exit, maxsize
from datetime import datetime
from time import sleep

arg_parser = argparse.ArgumentParser(prog=u'fcdsim')
arg_parser.add_argument('host',
                        metavar='HOST',
                        help='Host to send the simulated Floating Car Data to')
arg_parser.add_argument('port',
                        metavar='PORT',
                        type=int,
                        help='TCP port to send the simulated Floating Car Data to')
arg_parser.add_argument('-b', '--base-fcd-only',
                        action='store_true',
                        help='Only send base FCD to host.')
arg_parser.add_argument('-r', '--requests-per-second',
                        type=int,
                        default=100,
                        metavar='NUM_REQUESTS',
                        help='The overall number of requests per second to send to the host. Default: 100')
arg_parser.add_argument('-f', '--faulty-data-per-second',
                        type=int,
                        default=10,
                        metavar='NUM_FAULTY',
                        help='The maximum number of requests per second, which contains faulty Floating Car Data. \
                        This is limited by the overall number of requests allowed. Default: 10')


class FCDBase(object):
    """

    """

    DEFAULT_CHOICES = [1, 1, 1, 1, 3, 5, ]

    def __init__(self):
        self.id = None
        self.speed = None
        self.timestamp = None
        self.longitude = None
        self.latitude = None

    def generate(self):
        """

        :return:
        """
        self.id = str(random.randint(1, 999999))
        self.speed = '{:.2f}'.format(random.uniform(0., 350.))
        self.timestamp = str(datetime.now().replace(microsecond=0))
        # Coordinates located worldwide
        # self.longitude = '{:.8f}'.format(random.uniform(-180., 180.))
        # self.latitude = '{:.8f}'.format(random.uniform(-90., 90.))
        # Coordinates located in Germany (more or less)
        self.longitude = '{:.8f}'.format(random.uniform(6., 15.))
        self.latitude = '{:.8f}'.format(random.uniform(47., 55.))

    def generate_errors(self, choices=DEFAULT_CHOICES):
        """

        :param choices:
        :return:
        """
        number_of_errors = random.choice(choices)
        counter = 0
        # we do not want to alter the id so remove it
        fields = self.__dict__.copy()
        del fields['id']
        while counter < number_of_errors:
            error_key = random.choice(fields.keys())
            # if 'speed' is chosen, alter it to a irrational high number in most cases (chance: 2/3)
            if error_key == 'speed' and random.choice([True, True, False]):
                self.speed = '{:.2f}'.format(random.uniform(350., 800.))
            # in every other case simply remove the value
            else:
                self.__dict__[error_key] = ''
            counter += 1

    def __str__(self):
        # Precision of Decimal expressed degrees, see: https://en.wikipedia.org/wiki/Decimal_degrees
        return ','.join([self.id,
                         self.speed,
                         self.timestamp,
                         self.longitude,
                         self.latitude])


class TaxiFCD(FCDBase):
    """

    """

    DEFAULT_CHOICES = [1, 1, 1, 1, 1, 1, 3, 5, 7, ]

    def __init__(self):
        super(TaxiFCD, self).__init__()
        self.taxi_id = None
        self.waiting_state = None
        self.busy_state = None
        self.gps_state = None
        self.degree = None

    def generate(self):
        super(TaxiFCD, self).generate()
        self.taxi_id = str(random.randint(1, 999999))
        self.waiting_state = str(random.choice([0, 1]))
        self.busy_state = str(random.choice([0, 1]))
        self.gps_state = str(random.choice([0, 1]))
        self.degree = '{:.0f}'.format(random.uniform(0, 360))

    def generate_errors(self, choices=DEFAULT_CHOICES):
        super(TaxiFCD, self).generate_errors(choices)

    def get_base_str(self):
        return super(TaxiFCD, self).__str__()

    def __str__(self):
        return ','.join([self.id,
                         self.taxi_id,
                         self.timestamp,
                         self.longitude,
                         self.latitude,
                         self.waiting_state,
                         self.busy_state,
                         self.degree,
                         self.speed,
                         self.gps_state, ])


def __main__():
    args = arg_parser.parse_args()

    spark_socket = None
    try:
        spark_socket = socket.create_connection((args.host, args.port))
    except OSError, e:
        print(e.strerror)
        exit(1)
    # deprecated, see https://docs.python.org/3.6/library/socket.html#socket.error
    except socket.error, e:
        print(e.strerror)
        exit(1)

    rps = args.requests_per_second
    if rps > 10000:
        rps = 10000
    tick = 1. / rps * 0.725
    fps = args.faulty_data_per_second
    if fps > rps:
        fps = rps
    mod = rps / fps if fps > 0 else rps
    sleeping = 0
    counter = 0
    fcd = TaxiFCD()

    print('Sending {} requests per second to {}:{}. Use CMD+c to stop the program.'.format(rps, args.host, args.port))
    program_start = datetime.now()
    try:
        while True:
            if counter == maxsize:
                counter = 0
            start = datetime.now()
            fcd.generate()
            if not counter % mod:
                fcd.generate_errors([1])
            if args.base_fcd_only or random.choice([True, False, False, False]):
                spark_socket.send(fcd.get_base_str())
            else:
                spark_socket.send(str(fcd))
            spark_socket.send('\n')
            sleeping += tick - (datetime.now() - start).total_seconds()
            if sleeping > 0:
                sleep(sleeping)
                sleeping = 0.
            counter += 1
    except OSError, e:
        print(e.strerror)
        exit(1)
    # deprecated, see https://docs.python.org/3.6/library/socket.html#socket.error
    except socket.error, e:
        print(e.strerror)
        exit(1)
    except KeyboardInterrupt:
        program_runtime = (datetime.now() - program_start).total_seconds()
        print('\n{} requests send in {}s (~{:.0f} requests per second)'.format(counter,
                                                                               program_runtime,
                                                                               counter/program_runtime))
    exit(0)
