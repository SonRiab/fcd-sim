import argparse
import random
from datetime import datetime

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
                        help='The number of requests per second, which contains faulty Floating Car Data. This is \
                        limited by the overall number of requests allowed. Default: 10')


class FCDBase(object):
    def __init__(self):
        self.id = None
        self.speed = None
        self.timestamp = None
        self.longitude = None
        self.latitude = None

    def generate(self):
        self.id = random.randint(1, 999999)
        self.speed = random.uniform(0., 250.)
        self.timestamp = datetime.now().replace(microsecond=0)
        # Coordinates located worldwide
        # self.longitude = random.uniform(-180., 180.)
        # self.latitude = random.uniform(-90., 90.)
        # Coordinates located in Germany (more or less)
        self.longitude = random.uniform(6., 15.)
        self.latitude = random.uniform(47., 55.)

    def __str__(self):
        # Precision of Decimal expressed degrees, see: https://en.wikipedia.org/wiki/Decimal_degrees
        return '{},{:.2f},{},{:.8f},{:.8f}'.format(self.id,
                                                   self.speed,
                                                   self.timestamp,
                                                   self.longitude,
                                                   self.latitude,)


class TaxiFCD(FCDBase):

    def __init__(self):
        super(TaxiFCD, self).__init__()
        self.taxi_id = None
        self.states = {
            'waiting': None,
            'busy': None,
            'gps': None,
        }
        self.degree = None

    def generate(self):
        super(TaxiFCD, self).generate()
        self.taxi_id = random.randint(1, 999999)
        self.states['waiting'] = random.choice([0, 1])
        self.states['busy'] = random.choice([0, 1])
        self.states['gps'] = random.choice([0, 1])
        self.degree = random.uniform(0, 360)

    def __str__(self):
        return '{},{},{},{:.8f},{:.8f},{},{},{},{:.2f},{}'.format(self.id,
                                                                  self.taxi_id,
                                                                  self.timestamp,
                                                                  self.longitude,
                                                                  self.latitude,
                                                                  self.states['waiting'],
                                                                  self.states['busy'],
                                                                  self.degree,
                                                                  self.speed,
                                                                  self.states['gps'],)


def __main__():
    # TODO remove or reuse this in later stages. for testing only at the moment.
    base_fcd = FCDBase()
    base_fcd.generate()
    print(base_fcd)
    taxi_fcd = TaxiFCD()
    taxi_fcd.generate()
    print(taxi_fcd)
    # TODO create and send FCD to host
    # args = arg_parser.parse_args()
