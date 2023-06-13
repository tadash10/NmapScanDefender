# NmapScanDefender

Improvements made to the script v2.py include:

    Logging: Implemented a logging mechanism using the logging module to record Nmap scan detections and script execution events. Logs are saved to a file named "nmap_defender.log" in the same directory as the script.

    Clearing iptables Rule: Added a function to clear the iptables rule that blocks Nmap scans. This ensures that the rule is removed even if the script is terminated unexpectedly, preventing any unintended blockages.

    Separate Functions: Split the script into separate functions for better organization, modularity, and reusability.

    Setup Logging Function: Created a function to configure the logging parameters, including the log format, log level (set to WARNING), and log file name.

    ISO Standard Compliance: The script adheres to standard Python coding practices, such as using subprocess.run() to execute system commands instead of os.system(), and adopting a standardized logging format.
