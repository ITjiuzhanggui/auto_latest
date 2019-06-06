import json
import time
from six import add_metaclass
from abc import ABCMeta, abstractmethod, abstractproperty
from conf import ConfManagement
from logs import SetLog

@add_metaclass(ABCMeta)
class Global(object):

    def read_logs(self, file_name):
        with open(file_name, 'r') as f:
            return f.readlines()

    @abstractproperty
    def serialization(self):
        pass

    # @abstractproperty
    # def save(self):
    #     pass

    def exception_to_response(self, match_result, message):
        if match_result == []:
            SetLog().info(" %s Not getting" % message)

def exect_contest(fun):
    try:
        return fun()
    except Exception as e:
        pass
