"""
Jordan Robert Blaker-Hood NCS-203 Practical
This Python file contains the code for the port scanner.
"""
# Imports
from queue import Queue
from socket import *
import threading
from datetime import *

# Variables
target = '127.0.0.1'
queue = Queue()
port_scan = []
current_date_time = datetime.now()


# This function creates a network socket, and then it attempts to connect to the specified ports on the target
def portscan(port):
    try:
        network_socket = socket(AF_INET, SOCK_STREAM)
        network_socket.connect((target, port))
        return True
    except:
        return False


# This function gets the ports to be used for the port scanner
def get_ports(mode):
    if mode == 1:
        for port in range(1, 1024):
            queue.put(port)


# This functions prints out the open ports and appends them to a list
def thread_worker():
    while not queue.empty():
        port = queue.get()
        if portscan(port):
            print("Port {} is open ".format(port))
            port_scan.append(port)
            with open('portscan-results.txt', 'w') as port_scan_file:
                port_scan_file.writelines(str(port_scan))


# This function runs the port scanner uses threads and taking in the mode to be used
def run_scanner(threads, mode):
    get_ports(mode)

    thread_list = []

    for thread in range(threads):
        thread = threading.Thread(target=thread_worker)
        thread_list.append(thread)

    for thread in thread_list:
        thread.start()

    for thread in thread_list:
        thread.join()


# This function starts the port scanner with 100 threads in mode 1
def run_portscan():
    run_scanner(100, 1)


if __name__ == '__main__':
    run_portscan()
