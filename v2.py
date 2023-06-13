import os
import sys
import socket
import logging
import subprocess

def set_iptables_rule():
    # Set iptables rule to block Nmap scans
    rule = "-A INPUT -p tcp --tcp-flags SYN,ACK SYN -m recent --name nmap --rcheck -j DROP"
    subprocess.run(["iptables", "-A", "INPUT", "-p", "tcp", "--tcp-flags", "SYN,ACK", "SYN",
                    "-m", "recent", "--name", "nmap", "--rcheck", "-j", "DROP"], check=True)
    logging.info("Nmap scan blocking rule added to iptables.")

def clear_iptables_rule():
    # Clear iptables rule to unblock Nmap scans
    subprocess.run(["iptables", "-D", "INPUT", "-p", "tcp", "--tcp-flags", "SYN,ACK", "SYN",
                    "-m", "recent", "--name", "nmap", "--rcheck", "-j", "DROP"], check=True)
    logging.info("Nmap scan blocking rule removed from iptables.")

def listen_for_nmap_scans(port):
    # Create a socket to listen for Nmap scans
    try:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(('0.0.0.0', port))
        listener.listen(1)
        logging.info("Listening for Nmap scans on port %d", port)
    except socket.error as e:
        sys.exit("Error creating the listening socket: " + str(e))

    # Accept incoming connections and log the attempts
    while True:
        try:
            client_socket, client_address = listener.accept()
            logging.warning("Nmap scan detected from: %s", client_address[0])
            client_socket.close()
        except socket.error as e:
            sys.exit("Error accepting incoming connection: " + str(e))

def setup_logging():
    # Configure logging parameters
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='nmap_defender.log', level=logging.WARNING, format=log_format)

def run_defender():
    # Set up logging
    setup_logging()

    # Check if the script is running with root privileges
    if os.geteuid() != 0:
        sys.exit("Please run this script as root.")

    try:
        set_iptables_rule()
        listen_for_nmap_scans(80)  # Change the port as required
    finally:
        clear_iptables_rule()

if __name__ == "__main__":
    run_defender()
