"""Jordan Robert Blaker-Hood NCS-203 Practical. This python file contains the abstract class NetworkSocket which is
subclassed by ServerCreation and ClientCreation. """
# Imports
from abc import ABC, abstractmethod
from datetime import *


# This class creates the abstract Network_Socket to be used by the ClientCreation class and the ServerCreation class
class NetworkSocket(ABC):
    host = '127.0.0.1'
    port = 3212
    end = None
    foreground = None
    txt = None
    current_date_time = datetime.now()
    current_date = current_date_time.strftime('%Y-%m-%d')
    current_time = current_date_time.strftime('%H:%M:%S')

    def __init__(self, host, port):
        self.host = host
        self.port = port

    # This creates the abstract function connection which is overridden in ServerCreation and ClientCreation
    @abstractmethod
    def connection(self):
        pass
