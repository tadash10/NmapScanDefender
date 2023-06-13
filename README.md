# NmapScanDefender
# Nmap Defender

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Nmap Defender is a Python script that helps defend against Nmap scans by blocking suspicious connections and providing additional security features. It can be used to enhance the security of your system and protect against potential threats.

## Features

- Block Nmap scans by adding an iptables rule.
- Log detected Nmap scans to a file.
- Whitelist specific IP addresses or ranges to allow authorized Nmap scans.
- Rate limit incoming connections from suspicious IP addresses.
- Integration with a Security Information and Event Management (SIEM) system (placeholder for future implementation).
- Dynamic port selection for listening (placeholder for future implementation).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/nmap-defender.git

Change into the project directory:cd nmap-defender

(Optional) Create and activate a virtual environment:                                               python -m venv venv
source venv/bin/activate


Install the required dependencies:
 pip install -r requirements.txt
 
 Usage

    Run the script as root:  sudo python nmap_defender.py

    The script will display a menu with the following options:
        Start Nmap Defender: Starts blocking Nmap scans and listening for connections.
        Whitelist IP Address: Whitelists a specific IP address or IP range to allow Nmap scans from.
        Set Rate Limit: Sets a rate limit for incoming connections from suspicious IP addresses.
        Quit: Exits the program.

    Select the desired option by entering the corresponding number.

Disclaimer

Please note that the effectiveness of this script may vary depending on your specific system and network configuration. It is recommended to review and adapt the script to meet your specific security requirements.
Contributing

Contributions to the Nmap Defender script are welcome! Please see the CONTRIBUTING.md file for more information.
 License

This project is licensed under the terms of the MIT License.
 
Improvements made to the script v2.py include:

    Logging: Implemented a logging mechanism using the logging module to record Nmap scan detections and script execution events. Logs are saved to a file named "nmap_defender.log" in the same directory as the script.

    Clearing iptables Rule: Added a function to clear the iptables rule that blocks Nmap scans. This ensures that the rule is removed even if the script is terminated unexpectedly, preventing any unintended blockages.

    Separate Functions: Split the script into separate functions for better organization, modularity, and reusability.

    Setup Logging Function: Created a function to configure the logging parameters, including the log format, log level (set to WARNING), and log file name.

    ISO Standard Compliance: The script adheres to standard Python coding practices, such as using subprocess.run() to execute system commands instead of os.system(), and adopting a standardized logging format.
