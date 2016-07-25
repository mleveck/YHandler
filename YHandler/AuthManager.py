import json
import csv
from abc import ABCMeta, abstractmethod


class AuthManager:
    """
    Abastract Base Authorization Manager Class
    Can be used to create additional configuration formats by overriding the below abstract methods
    """
    __metaclass__ = ABCMeta

    def __init__(self, authf):
        self.authf = authf

    @abstractmethod
    def get_authvals(self):
        pass

    @abstractmethod
    def write_authvals(self, authd):
        pass


class CSVAuthManager(AuthManager):
    """
    Authorization Manager for CSV files
    """

    def __init__(self, authf):
        super(CSVAuthManager, self).__init__(authf)

    def get_authvals(self):
        """
        Read authorization parameters from the csv authorization file
        :return: a dictionary containing oauth parameters
        """
        vals = {}  # dict of vals to be returned
        with open(self.authf, 'rb') as f:
            f_iter = csv.DictReader(f)
            vals = f_iter.next()
        return vals

    def write_authvals(self, authd):
        f = open(self.authf, 'wb')
        fieldnames = tuple(authd.iterkeys())
        headers = dict((n, n) for n in fieldnames)
        f_iter = csv.DictWriter(f, fieldnames=fieldnames)
        f_iter.writerow(headers)
        f_iter.writerow(authd)
        f.close()


class JsonAuthManager(AuthManager):
    """
    Authorization Manager for Json files
    """

    def __init__(self, authf):
        super(JsonAuthManager, self).__init__(authf)

    def get_authvals(self):
        """
        Read authorization parameters from the json authorization file
        :return: a dictionary containing oauth parameters
        """
        with open(self.authf) as f:
            result = json.load(f)
        return result

    def write_authvals(self, authd):
        with open(self.authf, 'wb') as f:
            json.dump(authd, f)
