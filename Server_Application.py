"""
Jordan Robert Blaker-Hood NCS-203 Practical. This python file contains the following subclasses ServerCreation and
ServerGui.
"""
# Imports
import linecache
from socket import *
from time import sleep
import tkinter as tk
from tkinter import ttk
import datetime
from threading import Thread
from networksocket import NetworkSocket
from gui_class import Gui
from subprocess import Popen

# Variable to be used to store Server chat
chat_log = []


# This creates the subclass ServerCreation of the abstract NetworkSocket class
class ServerCreation(NetworkSocket):
    # Empty Host and Port Attributes as these parameters will be passed in when creating object.
    # Sock defined in Attribute as a socket connection using TCP and IPv4.
    host = '127.0.0.1'
    port = 3212
    server_socket = socket(AF_INET, SOCK_STREAM)  # creates attribute server_socket to bind host and port together to
    # receive data  from client
    custom_socket = socket(AF_INET, SOCK_STREAM)  # creates attribute custom_socket for sending custom server
    # message to client using a new port
    default_socket = socket(AF_INET, SOCK_STREAM)  # creates attribute default_socket for sending server default
    # message to client using a new port
    end = "end"  # overrides attribute end in abstract class NetworkSocket
    txt = ".txt"  # overrides attribute txt in abstract class NetworkSocket
    line = 1  # creates attribute line to be used by linecache to extract data from txt files
    open_ports = None  # creates attribute open_ports to be used to store list of open ports to be displayed in chat

    # Constructor to assign parameters passed into object to self, to be used in the sock.bind command.
    def __init__(self, host, port):
        super().__init__(host, port)
        self.host = host
        self.port = port

    # Overrides method connection in abstract class NetworkSocket, binds port 3212 with host 127.0.0.1 to receive
    # client request code to determine which information to receive that the client has sent
    def connection(self):
        print(f"Starting up connection on Port: {self.port} and Host Address: {self.host}")
        my_server_gui.connection_lbl.config(text="Successfully Connected!", foreground="green")
        self.add_text(f"Connection Initiated on {self.current_date} at {self.current_time}")
        # Sock.bind command binds connection to predefined port and host.
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(2)
        (connection, clientAddress) = self.server_socket.accept()
        self.add_text(f"Connection received from:{clientAddress}")
        while True:
            try:
                data = connection.recv(1024)
                decoded = data.decode('utf-8')
                print(f"Received Client Request Code: {decoded}")
                # RECEIVING IP ADDRESS when client request code 1 is recieved by the server
                if str(decoded) == "1":
                    data_ip = connection.recv(1024)
                    decoded_ip = data_ip.decode('utf-8')  # decodes the recieved ip address into utf-8
                    self.add_text(f"{self.current_time}: Client's IP Address: {decoded_ip}")
                # RECEIVING MAC ADDRESS when client request code 2 is recieved by the server
                elif str(decoded) == "2":
                    data_mac = connection.recv(1024)
                    decoded_mac = data_mac.decode('utf-8')  # decodes the recieved mac address into utf-8
                    self.add_text(f"{self.current_time}: Client's Mac Address: {decoded_mac}")
                # RECEIVING RUNNING PROCESSES when client request code 3 is recieved by the server
                elif str(decoded) == "3":
                    data_processes = connection.recv(15000)
                    decoded_processes = data_processes.decode('utf-8')  # decodes the recieved running processes into
                    # utf-8
                    self.add_text(f"{self.current_time}: Client's Running Processes: {decoded_processes}")
                # RECEIVING UPTIME when client request code 4 is recieved by the server
                elif str(decoded) == "4":
                    data_uptime = connection.recv(1024)
                    decoded_uptime = data_uptime.decode('utf-8')  # decodes the recieved uptime into utf-8
                    self.add_text(f"{self.current_time}: Client's current Up Time: {decoded_uptime} seconds")
                # RECEIVING PC NAME when client request code 5 is recieved by the server
                elif str(decoded) == "5":
                    data_pcname = connection.recv(1024)
                    decoded_pc_name = data_pcname.decode('utf-8')  # decodes the recieved pc name into utf-8
                    self.add_text(f"{self.current_time}: Client's PC Name: {decoded_pc_name}")
                # RECEIVING DEFAULT MESSAGE when client request code 6 is recieved by the server
                elif str(decoded) == "6":
                    client_default_msg = connection.recv(1024)
                    client_default_msg_decoded = client_default_msg.decode('utf-8')  # decodes the client default
                    # message into utf-8
                    self.add_text(f"{self.current_time}: Client: {client_default_msg_decoded}")
                # RECEIVING CUSTOM MESSAGE when client request code 7 is recieved by the server
                elif str(decoded) == "7":
                    client_custom_msg = connection.recv(1024)
                    client_custom_msg_decoded = client_custom_msg.decode('utf-8')  # decodes the client custom
                    # message into utf-8
                    self.add_text(f"{self.current_time}: Client: {client_custom_msg_decoded}")
                    # RECEIVING MESSAGE THAT CLIENT IS LEAVING when client request code 8 is recieved by the server
                elif str(decoded) == "8":
                    leaving = connection.recv(1024)
                    leaving_decoded = leaving.decode('utf-8')  # decodes the client leaving message into utf-8
                    self.add_text(f"{self.current_time}: Client: {leaving_decoded}")
            except socket.error as error:
                print(f"Error: {error}")

    # This method sends the server default message to the client using a new port
    def send_default(self):
        while True:
            self.default_socket.bind(('127.0.0.1', 3213))  # binds 127.0.0.1 with port 3213
            self.default_socket.listen(2)
            (connection, client_address) = self.default_socket.accept()
            sleep(1)
            server_default_msg = "This is a default message from the Server."
            encoded_default_msg = str(server_default_msg).encode()  # encodes server default message into bytes
            print(encoded_default_msg)
            connection.sendall(encoded_default_msg)
            break

    # This method sends a custom message to the client using a new port
    def send_custom(self):
        while True:
            self.custom_socket.bind(('127.0.0.1', 3214))  # binds 127.0.0.1 with port 3214
            self.custom_socket.listen(2)
            (connection, client_address) = self.custom_socket.accept()
            sleep(1)
            server_custom_msg = my_server_gui.custom_message.get()  # gets the custom message from the text entry box
            server_encoded_custom_msg = str(server_custom_msg).encode()  # encodes server custom message into bytes
            print(server_encoded_custom_msg)
            connection.sendall(server_encoded_custom_msg)
            break

    # This method saves the entire server chat log into a text file with the date as part of the filename
    def save_info(self):
        filename = 'Server chat Log'
        file_date = datetime.datetime.now()
        with open(filename + file_date.strftime('%d %B %Y') + self.txt, 'w') as file:
            file.write('______Server chat Log______  ')
            file.write('\n')
            file.write('\n'.join(chat_log))
            file.write('\n')
        print("Saved to File.")

    # This method adds text to the server text box
    def add_text(self, data):
        my_server_gui.server_gui_chat.insert(self.end, f"\n{data}")
        my_server_gui.server_gui.update()
        # data appended to list here:
        chat_log.append(data)

    # This method will disconnect the socket connection
    def disconnect(self):
        # Only used for the Quit Button.
        self.add_text("Server is Disconnecting, please wait...")
        sleep(2)
        self.server_socket.close()
        my_server_gui.server_gui.destroy()

    # This method sets the open ports from the portscan-results txt file into the attribute open_ports
    def set_open_ports(self):
        open_ports_data = linecache.getline('portscan-results.txt', self.line)
        open_ports = open_ports_data.rstrip('\n')
        client_open_ports = open_ports
        self.open_ports = client_open_ports
        return self.open_ports

    # This method displays the results of the port scan using the attribute open_ports and the method add_text
    def display_client_open_ports(self):
        ports = self.set_open_ports()
        self.add_text(f"{self.current_time}: Open ports on client: {ports}")


# Creating Server objects  and thread
myServer = ServerCreation('127.0.0.1', 3212)
threadSocket = Thread(target=myServer.connection)

send_default = ServerCreation('127.0.0.1', 3213)
send_custom = ServerCreation('127.0.0.1', 3214)


#   This creates the subclass ServerGui of the abstract class Gui
class ServerGui(Gui):
    server_gui = tk.Tk()
    title = 'Server Application'  # overrides attribute in abstract Gui class, sets title to Server Application
    application_frame = ttk.Frame(server_gui)  # overrides attribute in abstract Gui class, creates frame for where
    # the labels and buttons go
    server_gui_chat = tk.Text(application_frame, height=20, width=70)  # creates attribute server_gui_chat to
    # display recieved data
    connection_lbl = ttk.Label(application_frame, text="No Connection with Client.", foreground="red")  # creates
    # attribute connection_lbl to show connection status
    chat = []
    custom_message = tk.StringVar()  # creates attribute custom_message as a string variable

    #   overrides method app() in abstract Gui Class
    def app(self):
        self.server_gui.geometry(self.app_size)  # configures application size
        self.server_gui.title(self.title)  # sets title of the application
        self.server_gui.iconbitmap(self.icon)  # sets icon for the application
        style = ttk.Style(self.server_gui)  # configures style for the application
        self.server_gui.tk.call('source', 'proxttk-dark.tcl')
        style.theme_use(self.theme)  # configures theme to be used by the application

        self.application_frame.grid(sticky=self.sticky)
        self.application_frame.columnconfigure(0, weight=1)

        # Creating labels for the server application
        title_lbl = ttk.Label(self.application_frame, text="SERVER APPLICATION", padding=self.padding)
        title_lbl.grid(row=1, column=2)

        self.connection_lbl.grid(row=2, column=3)

        default_msg_lbl = ttk.Label(self.application_frame, text="This is a default message from the Server!")
        default_msg_lbl.grid(row=3, column=3, sticky=self.sticky)

        self.server_gui_chat.grid(row=6, columnspan=12, sticky=self.sticky)

        # Creating a  scroll Bar for the server application
        scroll = ttk.Scrollbar(self.application_frame, command=self.server_gui_chat.yview)
        scroll.grid(row=6, column=4, sticky=self.sticky)
        self.server_gui_chat['yscrollcommand'] = scroll.set

        # Creating  text Entry for custom message
        custom_msg_entry = ttk.Entry(self.application_frame, width=10, textvariable=self.custom_message)
        custom_msg_entry.grid(row=4, column=3, sticky=self.sticky)

        # Creating Buttons for the server application with lambda used to run the commands only when the button is
        # pressed
        connect_btn = ttk.Button(self.application_frame, text="Initiate Connection", padding=self.padding,
                                 style=self.style,
                                 command=lambda: threadSocket.start())
        connect_btn.grid(row=2, column=1)

        default_msg_btn = ttk.Button(self.application_frame, text="Send Default Message:", style=self.style,
                                     padding=self.padding,
                                     command=lambda: send_default.send_default())
        default_msg_btn.grid(row=3, column=1, sticky=self.sticky)

        custom_msg_btn = ttk.Button(self.application_frame, text="Send Custom Message:", style=self.style,
                                    padding=self.padding,
                                    command=lambda: send_custom.send_custom())
        custom_msg_btn.grid(row=4, column=1, sticky=self.sticky)

        portscan_btn = ttk.Button(self.application_frame, text="Run Port Scan", padding=self.padding, style=self.style,
                                  command=lambda: Popen('Python fast_portscan.py'))
        portscan_btn.grid(row=5, column=1, sticky=self.sticky)

        show_portscan_results = ttk.Button(self.application_frame, text='Show Port Scan Results', padding=self.padding,
                                           style=self.style, command=lambda: myServer.display_client_open_ports())
        show_portscan_results.grid(row=5, column=2, sticky=self.sticky)

        save_text_btn = ttk.Button(self.application_frame, text="Save to Text File", padding=self.padding,
                                   style=self.style,
                                   command=lambda: myServer.save_info())
        save_text_btn.grid(row=7, column=1, sticky=self.sticky)

        quit_btn = ttk.Button(self.application_frame, text="Exit Application", padding=self.padding, style=self.style,
                              command=lambda: myServer.disconnect())
        quit_btn.grid(row=7, column=3, sticky=self.sticky)

        self.server_gui.mainloop()


# creates ServerGui object
my_server_gui = ServerGui()

if __name__ == '__main__':
    my_server_gui.app()
