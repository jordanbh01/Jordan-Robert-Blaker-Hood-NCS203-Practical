"""
NCS-203 Jordan Robert Blaker-Hood Practical
This python file contains the ClientExtract class which gets the client's hostname,ip address and mac address.
"""
import socket
import os
import sys
from uptime import uptime
import wmi as windows
from threading import *


# This creates the Class ClientExtract with the following attributes' computer_name,mac_address,ip_address
class ClientExtract:
    _computer_name = ''
    _mac_address = ''
    _ip_address = ''

    def __init__(self, mac_address, ip_address, computer_name):

        self._computer_name = computer_name
        self._mac_address = mac_address
        self._ip_address = ip_address

    # This method gets the computername of the client and then writes the computer name to a textfile
    def get_computername(self):
        self._computer_name = socket.gethostname()
        print(f"Hostname of client: {self._computer_name}")
        computername = open('client extracted information/client_extractcomputername.txt', 'w')
        computername.writelines(self._computer_name)
        return self._computer_name

    # This method gets the ip address of the client and then writes the ip address to a textfile
    def get_ip(self):
        self._ip_address = socket.gethostbyname(self._computer_name)
        print(f"IP address of client: {self._ip_address}")
        ip = open('client extracted information/client_extractip.txt', 'w')
        ip.writelines(self._ip_address)
        return self._ip_address

    # This method gets the mac address of the client and then writes the mac address to a textfile
    def get_mac(self):
        if sys.platform == 'win32':
            for line in os.popen('ipconfig /all'):
                if line.lstrip().startswith('Physical Address'):
                    self._mac_address = line.split(':')[1].strip().replace('-', ':')
                    break

        else:
            for line in os.popen('/sbin/ipconfig'):
                if line.find('Ether') > -1:
                    self._mac_address = line.split()[4]
                    break

        print(f"MAC ADDRESS of client:{self._mac_address}")
        mac = open('client extracted information/client_extractmac.txt', 'w')
        mac.writelines(self._mac_address)
        return self._mac_address


# This function runs the methods inside the class ClientExtract
def run_extract_computername_ip_mac():
    client_extract1 = ClientExtract('mac_address', 'ip_address', 'computer_name')
    client_extract1.get_computername()
    client_extract1.get_ip()
    client_extract1.get_mac()


# This function gets the uptime of the client and then writes it to a textfile
def run_uptime():
    client_uptime = uptime()
    print(f"Client uptime : {client_uptime} seconds")
    up = open('client extracted information/client_extractuptime.txt', 'w')
    up.writelines(str(client_uptime))


# This function gets the running processes of the client and then writes it to a textfile
def get_running_processes():
    p = windows.WMI()
    file = open('client extracted information/client_extractprocess.txt', 'w')
    for process in p.Win32_Process():
        file.writelines(process.Name + "\n")
        print(process.Name)


# This function run all the functions for client_extract which is used by the Get client information button which
# uses Popen to run this function
def run():
    run_extract_computername_ip_mac()
    run_uptime()
    get_running_processes()


if __name__ == '__main__':
    run()
