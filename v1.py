import os
import sys
import socket

def block_nmap_scans():
    # Check if the script is running with root privileges
    if os.geteuid() != 0:
        sys.exit("Please run this script as root.")

    # Block incoming Nmap scans using iptables
    iptables_rule = "-A INPUT -p tcp --tcp-flags SYN,ACK SYN -m recent --name nmap --rcheck -j DROP"
    iptables_command = f"iptables {iptables_rule}"
    os.system(iptables_command)
    print("Nmap scan blocking rule added to iptables.")

def detect_nmap_scans():
    # Create a socket to listen for Nmap scans
    listening_port = 80  # Choose a port that is commonly scanned
    try:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(('0.0.0.0', listening_port))
        listener.listen(1)
        print("Listening for Nmap scans on port", listening_port)
    except socket.error as e:
        sys.exit("Error creating the listening socket: " + str(e))

    # Accept incoming connections and log the attempts
    while True:
        try:
            client_socket, client_address = listener.accept()
            print("Nmap scan detected from:", client_address)
            client_socket.close()
        except socket.error as e:
            sys.exit("Error accepting incoming connection: " + str(e))

if __name__ == "__main__":
    block_nmap_scans()
    detect_nmap_scans()
