"""
This python file contains the pytest test for client_extract
"""
import client_extract
import linecache
import socket


def test_get_computername():
    client_extract1 = client_extract.ClientExtract('mac_address', 'ip_address', 'computer_name')
    test_hostname = client_extract1.get_computername()
    hostname_data = linecache.getline('client extracted information/client_extractcomputername.txt', 1)
    hostname = hostname_data.rstrip('\n')
    assert hostname == test_hostname


def test_get_ip():
    hostname_data = linecache.getline('client extracted information/client_extractcomputername.txt', 1)
    hostname = hostname_data.rstrip('\n')
    test_ip = socket.gethostbyname(hostname)
    ip_data = linecache.getline('client extracted information/client_extractip.txt', 1)
    ip = ip_data.rstrip('\n')
    assert ip == test_ip


def test_get_mac():
    client_extract2 = client_extract.ClientExtract('mac_address', 'ip_address', 'computer_name')
    test_mac = client_extract2.get_mac()
    mac_data = linecache.getline('client extracted information/client_extractmac.txt', 1)
    mac = mac_data.rstrip('\n')
    assert mac == test_mac


def test_get_uptime():
    test_uptime = client_extract.run_uptime()
    uptime_data = linecache.getline('client extracted information/client_extractuptime.txt', 1)
    uptime = uptime_data.rstrip('\n')
    assert uptime == test_uptime


def test_get_running_process():
    test_running_process = client_extract.get_running_processes()
    with open('client extracted information/client_extractprocess.txt', 'r') as process_data:
        process = process_data.read()
    running_process = process.rstrip('\n')
    assert running_process == test_running_process
