"""
Jordan Robert Blaker-Hood NCS-203 Practical. This python files contains the subclass ClientCreation and ClientGui.
"""
# Imports
from socket import *
from time import sleep
import tkinter as tk
from tkinter import ttk
from threading import Thread
from networksocket import NetworkSocket
from gui_class import Gui
import linecache
import datetime
from subprocess import Popen

# Variable to store client chat log in a list
client_chat_log = []


# This creates the subclass ClientCreation of the abstract NetworkSocket class
class ClientCreation(NetworkSocket):
    host = str('127.0.0.1')  # overrides the attribute host in the abstract class NetworkSocket
    port = 3212  # overrides the attribute port in the abstract class NetworkSocket
    client_socket = socket(AF_INET, SOCK_STREAM)  # creates the attribute client_socket to create the socket
    # connection to the server
    __mac_address = None
    __ip_address = None
    __hostname = None
    __upTime = None
    line = 1
    end = 'end'  # overrides the attribute end in the abstract class NetworkSocket
    foreground = 'green'  # overrides the attribute foreground in the abstract class NetworkSocket
    txt = ' .txt'
    date = datetime.datetime.now()

    # Constructor to assign parameters passed into class as the IP Address and Port for Socket Connection.

    def __init__(self, host, port):
        super().__init__(host, port)
        self.host = host
        self.port = port

    # This method sets the mac address of the client by using linecache to read the mac address in the text file and
    # sets the data as the private mac_address attribute
    def set_mac_address(self):
        mac_data = linecache.getline('client extracted information/client_extractmac.txt', self.line)
        mac = mac_data.rstrip('\n')
        self.__mac_address = mac
        return self.__mac_address

    # This method sets the ip address of the client by using linecache to read the ip address in the text  file and
    # sets the ip address as the private attribute ip_address
    def set_ip_address(self):
        ip_data = linecache.getline('client extracted information/client_extractip.txt', self.line)
        ip = ip_data.rstrip('\n')
        self.__ip_address = ip
        return self.__ip_address

    # This method sets the hostname of the client by using linecache to read the hostname in the text file and sets
    # the hostname as the private attribute hostname
    def set_hostname(self):
        hostname_data = linecache.getline('client extracted information/client_extractcomputername.txt', self.line)
        hostname = hostname_data.rstrip('\n')
        self.__hostname = hostname
        return self.__hostname

    # This method sets the uptime of the client by using linecache to read the uptime in the text file and sets
    # the hostname as the private attribute uptime
    def set_client_uptime(self):
        uptime_data = linecache.getline('client extracted information/client_extractuptime.txt', self.line)
        uptime = uptime_data.rstrip('\n')
        self.__upTime = uptime
        return self.__upTime

    #   overrides method connection in abstract class NetworkSocket
    def connection(self):
        print(f"Connecting to Address: {self.host} Port: {self.port}")
        my_client_gui.lbl_Connection.config(text="Successfully Connected!", foreground=self.foreground)
        self.add_text(f"Connection Initiated on {self.current_date} at {self.current_time}")
        self.client_socket.connect((self.host, self.port))  # connects the client to the host and port
        while True:
            try:
                data = self.client_socket.recv(1024)
                decoded = data.decode('utf-8')
                print(f"Recieved Client Request Code: {decoded}")
                if str(decoded) == "1":
                    dataDefault = self.client_socket.recv(1024)
                    decodedMessage = dataDefault.decode('utf-8')
                    print(f"Server: {decodedMessage}")
                if str(decoded) == "2":
                    dataCustom = self.client_socket.recv(1024)
                    decodedMessage = dataCustom.decode('utf-8')
                    print(f"Server: {decodedMessage}")
            except socket.error as error:
                print(f"Error: {error}")

    # This method sends the client ip address to the server and uses a number to identify what is sent
    def send_client_ip_address(self):
        ip_identify = str(1).encode()
        self.client_socket.sendall(ip_identify)
        sleep(1)
        client_ip = self.set_ip_address()
        encoded_client_ip = str(client_ip).encode()
        print(encoded_client_ip)
        self.client_socket.sendall(encoded_client_ip)
        self.add_text(f"{self.current_time}: IP Address Sent.")

    # This method sends the client mac address to the server and uses a number to identify what is sent
    def send_client_mac_address(self):
        mac_identify = str(2).encode()
        self.client_socket.sendall(mac_identify)
        sleep(1)
        client_mac_address = self.set_mac_address()
        encoded_client_mac = str(client_mac_address).encode()
        print(encoded_client_mac)
        self.client_socket.sendall(encoded_client_mac)
        self.add_text(f"{self.current_time}: Mac Address Sent.")

    # This method send the client's running processes to the server and uses a number to identify what is sent
    def send_client_processes(self):
        while True:
            process_identify = str(3).encode()
            self.client_socket.sendall(process_identify)
            sleep(1)
            with open('client extracted information/client_extractprocess.txt', 'r') as process_data:
                process = process_data.read()
            print(process)
            encoded_process = str(process).encode()
            print(encoded_process)
            self.client_socket.sendall(encoded_process)
            sleep(1)
            self.add_text(f"{self.current_time}: Current Running Processes Sent.")
            break

    # This method sends the client's uptime to the server and uses a number to identify what is sent
    def send_client_uptime(self):
        uptime_identify = str(4).encode()
        self.client_socket.sendall(uptime_identify)
        sleep(1)
        client_uptime = self.set_client_uptime()
        encoded_client_uptime = str(client_uptime).encode()
        print(encoded_client_uptime)
        self.client_socket.sendall(encoded_client_uptime)
        self.add_text(f"{self.current_time}: Current Up Time Sent.")

    # This method sends the client's hostname to the server and uses a number to identify what is sent
    def send_client_hostname(self):
        while True:
            hostname_identify = str(5).encode()
            self.client_socket.sendall(hostname_identify)
            sleep(1)
            client_hostname = self.set_hostname()
            encoded_client_hostname = str(client_hostname).encode()
            print(encoded_client_hostname)
            self.client_socket.sendall(encoded_client_hostname)
            self.add_text(f"{self.current_time}: PC Name Sent.")
            break

    # This method sends the client's default message to the server and uses a number to identify what is sent
    def send_client_default_message(self):
        while True:
            default_msg_identify = str(6).encode()
            self.client_socket.sendall(default_msg_identify)
            sleep(1)
            client_default_msg = "This is a default message from the Client."
            encoded_client_default_msg = str(client_default_msg).encode()
            print(encoded_client_default_msg)
            self.client_socket.sendall(encoded_client_default_msg)
            self.add_text(f"{self.current_time}: Default Message Sent.")
            break

    # This method sends the client's custom message to the server and uses a number to identify what is sent
    def send_client_custom_message(self):
        while True:
            custom_msg_identify = str(7).encode()
            self.client_socket.sendall(custom_msg_identify)
            sleep(1)
            client_custom_msg = my_client_gui.customMessage.get()
            encoded_client_custom_msg = str(client_custom_msg).encode()
            print(encoded_client_custom_msg)
            self.client_socket.sendall(encoded_client_custom_msg)
            self.add_text(f"{self.current_time}: Message Sent.")
            break

    # This method receives the default message from server using new port
    def recv_default(self):
        default_sock = socket(AF_INET, SOCK_STREAM)
        default_sock.connect(('127.0.0.1', 3213))
        default_recv = default_sock.recv(1024)
        default_recv_decode = default_recv.decode('utf-8')
        print(default_recv_decode)
        self.add_text(f"{self.current_time}: Server: {default_recv_decode}")

    # This method receives custom message from server using new port
    def recv_custom(self):
        custom_sock = socket(AF_INET, SOCK_STREAM)
        custom_sock.connect(('127.0.0.1', 3214))
        custom_recv = custom_sock.recv(1024)
        custom_recv_decode = custom_recv.decode('utf-8')
        print(custom_recv_decode)
        self.add_text(f"{self.current_time}: Server: {custom_recv_decode}")

    # This method sends a message to the server that the client is disconnecting, uses a number to identify what is sent
    def send_leaving(self):
        while True:
            leaving_identify = str(8).encode()
            self.client_socket.sendall(leaving_identify)
            sleep(1)
            leaving_msg = "Closing socket connection, please wait..."
            encoded_leaving = str(leaving_msg).encode()
            self.client_socket.sendall(encoded_leaving)
            self.add_text(f"{self.current_time}: Closing connection with Server, please wait...")
            sleep(2)
            self.client_socket.close()
            my_client_gui.client_gui.destroy()

    # This method adds text to the textbox and appends data to a list
    def add_text(self, data):
        my_client_gui.client_txtbox.insert(self.end, f"\n{data}")
        my_client_gui.client_gui.update()
        # Appending chat to list
        client_chat_log.append(data)

    # This method saves the client chat log to a text file and uses the date as part of  the filename
    def save_info(self):
        client_filename = 'Client chat Log'
        client_file_date = self.date
        with open(client_filename + client_file_date.strftime('%d %B %Y') + self.txt, 'w') as client_file:
            client_file.write('_______Client chat Log______  ')
            client_file.write('\n')
            client_file.write('\n'.join(client_chat_log))
            client_file.write('\n')
        print("Saved to File.")


# Create Client Objects and Threads
myClient = ClientCreation('127.0.0.1', 3212)
threadSocket = Thread(target=myClient.connection)

recv_default = ClientCreation('127.0.0.1', 3213)

recv_custom = ClientCreation('127.0.0.1', 3214)


# This creates the subclass ClientGui of the abstract class Gui
class ClientGui(Gui):
    client_gui = tk.Tk()
    title = 'Client Application'  # overrides attribute title in abstract class Gui and sets title to Client Application
    customMessage = tk.StringVar()
    application_frame = ttk.Frame(client_gui)
    lbl_Connection = ttk.Label(application_frame, text="No connection with Server.",
                               foreground=Gui.connection_label_foreground)
    client_txtbox = tk.Text(application_frame, height=20, width=50)

    # Overrides method app() from abstract class Gui
    def app(self):
        self.client_gui.geometry(self.app_size)  # sets application size
        self.client_gui.title(self.title)  # sets application title
        self.client_gui.iconbitmap(self.icon)  # sets icon for the application
        style = ttk.Style(self.client_gui)
        self.client_gui.tk.call('source', 'proxttk-dark.tcl')
        style.theme_use('proxttk-dark')
        # Creating  Frames
        self.application_frame.grid(sticky=self.sticky)
        self.application_frame.columnconfigure(0, weight=1)

        # Creating labels for the client application
        title_lbl = ttk.Label(self.application_frame, text="CLIENT APPLICATION", padding=self.padding)
        title_lbl.grid(row=1, column=2)

        default_msg_lbl = ttk.Label(self.application_frame, text="This is a default message from the Client",
                                    padding=self.padding)
        default_msg_lbl.grid(row=3, column=3, sticky=self.sticky)

        self.lbl_Connection.grid(row=2, column=3)

        # Creating text entry for the client custom message
        custom_msg_entry = ttk.Entry(self.application_frame, width=10, textvariable=self.customMessage)
        custom_msg_entry.grid(row=5, column=3, sticky=self.sticky)

        # Creating Text Box and setting position of it in the application
        self.client_txtbox.grid(row=11, columnspan=6, sticky=self.sticky)

        # Creating  Scroll Bar for the application
        scroll = ttk.Scrollbar(self.application_frame, command=self.client_txtbox.yview)
        scroll.grid(row=8, column=4, sticky='nsew')
        self.client_txtbox['yscrollcommand'] = scroll.set

        # Create buttons for the application which use lambda for the command to ensure they only run when the button
        # is pressed
        get_client_information_btn = ttk.Button(self.application_frame, text='Get client information', style=self.style,
                                                padding=self.padding, command=lambda: Popen('Python client_extract.py'))
        get_client_information_btn.grid(row=2, column=1)
        connect_btn = ttk.Button(self.application_frame, text="Initiate Connection", style=self.style,
                                 padding=self.padding,
                                 command=lambda: threadSocket.start())
        connect_btn.grid(row=2, column=2)

        default_msg_btn = ttk.Button(self.application_frame, text="Send Default Message:", style=self.style,
                                     padding=self.padding,
                                     command=lambda: myClient.send_client_default_message())
        default_msg_btn.grid(row=3, column=2, sticky=self.sticky)

        custom_msg_btn = ttk.Button(self.application_frame, text="Send Custom Message:", style=self.style,
                                    padding=self.padding,
                                    command=lambda: myClient.send_client_custom_message())
        custom_msg_btn.grid(row=5, column=2, sticky=self.sticky)

        send_mac_btn = ttk.Button(self.application_frame, text="Send MAC Address", style=self.style,
                                  padding=self.padding,
                                  command=lambda: myClient.send_client_mac_address())
        send_mac_btn.grid(row=3, column=1, sticky=self.sticky)

        send_hostname_btn = ttk.Button(self.application_frame, text="Send hostname", style=self.style,
                                       padding=self.padding,
                                       command=lambda: myClient.send_client_hostname())
        send_hostname_btn.grid(row=4, column=2, sticky=self.sticky)

        send_ip_btn = ttk.Button(self.application_frame, text="Send IP Address", padding=self.padding, style=self.style,
                                 command=lambda: myClient.send_client_ip_address())
        send_ip_btn.grid(row=6, column=2, sticky=self.sticky)

        send_uptime_btn = ttk.Button(self.application_frame, text="Send System Up Time", style=self.style,
                                     padding=self.padding,
                                     command=lambda: myClient.send_client_uptime())
        send_uptime_btn.grid(row=4, column=1, sticky=self.sticky)

        send_process_btn = ttk.Button(self.application_frame, text="Send Running Processes", style=self.style,
                                      padding=self.padding,
                                      command=lambda: myClient.send_client_processes())
        send_process_btn.grid(row=7, column=2, sticky=self.sticky)

        btn_recv_default = ttk.Button(self.application_frame, text='Receive default message from server',
                                      style=self.style,
                                      padding=self.padding,
                                      command=lambda: recv_default.recv_default())
        btn_recv_default.grid(row=5, column=1, sticky=self.sticky)

        btn_recv_custom = ttk.Button(self.application_frame, text='Receive custom message from server',
                                     style=self.style,
                                     padding=self.padding,
                                     command=lambda: recv_custom.recv_custom())
        btn_recv_custom.grid(row=6, column=1, sticky=self.sticky)

        save_chat_btn = ttk.Button(self.application_frame, text='Save Info', style=self.style, padding=self.padding,
                                   command=lambda: myClient.save_info())
        save_chat_btn.grid(row=7, column=1, sticky=self.sticky)

        quit_btn = ttk.Button(self.application_frame, text="Exit Application", padding=self.padding, style=self.style,
                              command=lambda: myClient.send_leaving())
        quit_btn.grid(row=8, column=1, sticky=self.sticky)

        self.client_gui.mainloop()


# Creating ClientGui object
my_client_gui = ClientGui()

if __name__ == "__main__":
    my_client_gui.app()
    myClient.set_ip_address()
    myClient.set_hostname()
    myClient.set_mac_address()
    myClient.set_client_uptime()
