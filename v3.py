import os
import sys
import socket
import logging
import subprocess
import smtplib
from email.mime.text import MIMEText

def set_iptables_rule():
    # Set iptables rule to block Nmap scans
    rule = "-A INPUT -p tcp --tcp-flags SYN,ACK SYN -m recent --name nmap --rcheck -j DROP"
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-p", "tcp", "--tcp-flags", "SYN,ACK", "SYN",
                        "-m", "recent", "--name", "nmap", "--rcheck", "-j", "DROP"], check=True)
        logging.info("Nmap scan blocking rule added to iptables.")
    except subprocess.CalledProcessError as e:
        logging.error("Failed to set iptables rule: %s", str(e))

def clear_iptables_rule():
    # Clear iptables rule to unblock Nmap scans
    try:
        subprocess.run(["iptables", "-D", "INPUT", "-p", "tcp", "--tcp-flags", "SYN,ACK", "SYN",
                        "-m", "recent", "--name", "nmap", "--rcheck", "-j", "DROP"], check=True)
        logging.info("Nmap scan blocking rule removed from iptables.")
    except subprocess.CalledProcessError as e:
        logging.error("Failed to clear iptables rule: %s", str(e))

def listen_for_nmap_scans(port):
    # Create a socket to listen for Nmap scans
    try:
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.bind(('0.0.0.0', port))
        listener.listen(1)
        logging.info("Listening for Nmap scans on port %d", port)
    except socket.error as e:
        logging.error("Error creating the listening socket: %s", str(e))
        sys.exit("Error creating the listening socket: " + str(e))

    # Accept incoming connections and log the attempts
    while True:
        try:
            client_socket, client_address = listener.accept()
            logging.warning("Nmap scan detected from: %s", client_address[0])
            send_email_notification(client_address[0])
            client_socket.close()
        except socket.error as e:
            logging.error("Error accepting incoming connection: %s", str(e))
            sys.exit("Error accepting incoming connection: " + str(e))

def setup_logging():
    # Configure logging parameters
    log_format = "%(asctime)s - %(levelname)s - %(message)s"
    logging.basicConfig(filename='nmap_defender.log', level=logging.WARNING, format=log_format)

def send_email_notification(ip_address):
    # Send email notification to the administrator
    from_address = 'sender@example.com'
    to_address = 'admin@example.com'
    subject = 'Nmap Scan Detected'
    body = f'Nmap scan detected from IP address: {ip_address}'

    # Create the email message
    msg = MIMEText(body)
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject

    try:
        with smtplib.SMTP('smtp.example.com', 587) as smtp_server:
            smtp_server.starttls()
            smtp_server.login('username', 'password')
            smtp_server.send_message(msg)
            logging.info("Email notification sent")
    except smtplib.SMTPException as e:
        logging.error("Failed to send email notification: %s", str(e))

def whitelist_ip_address(ip_address):
    # Add the IP address to the whitelist
    try:
        subprocess.run(["iptables", "-I", "INPUT", "-s", ip_address, "-j", "ACCEPT"], check=True)
        logging.info("IP address whitelisted: %s", ip_address)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to whitelist IP address: %s", str(e))

def rate_limit_ip_address(ip_address, limit):
    # Rate limit incoming connections from the IP address
    try:
        subprocess.run(["iptables", "-I", "INPUT", "-p", "tcp", "-m", "state", "--state", "NEW",
                        "-m", "recent", "--set", "--name", "ratelimit", "--rsource"], check=True)
        subprocess.run(["iptables", "-I", "INPUT", "-p", "tcp", "-m", "state", "--state", "NEW",
                        "-m", "recent", "--update", "--name", "ratelimit", "--rsource", "--seconds", "60",
                        "--hitcount", str(limit), "-j", "DROP"], check=True)
        logging.info("Rate limiting set up for IP address: %s", ip_address)
    except subprocess.CalledProcessError as e:
        logging.error("Failed to set up rate limiting: %s", str(e))

def integrate_with_siem(event):
    # Send the event to the SIEM system for centralized monitoring
    siem_endpoint = 'https://siem.example.com/api/events'

    try:
        # Send the event data to the SIEM endpoint using appropriate request libraries or frameworks
        # Replace the following code with the actual implementation
        response = requests.post(siem_endpoint, json=event)
        if response.status_code == 200:
            logging.info("Event sent to SIEM system.")
        else:
            logging.error("Failed to send event to SIEM system. Status code: %d", response.status_code)
    except Exception as e:
        logging.error("Failed to send event to SIEM system: %s", str(e))

def dynamic_port_selection():
    # Implement the logic to dynamically select the listening port based on availability or configuration
    # Replace the following code with the actual implementation
    return 8080

def run_defender():
    # Set up logging
    setup_logging()

    # Check if the script is running with root privileges
    if os.geteuid() != 0:
        sys.exit("Please run this script as root.")

    try:
        set_iptables_rule()
        port = dynamic_port_selection()
        listen_for_nmap_scans(port)
    finally:
        clear_iptables_rule()

if __name__ == "__main__":
    run_defender()
