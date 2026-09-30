"""
Basic into script to test scrapli with textfsm parsing.  
This script will connect to a list of devices in devices.txt, 
run a list of commands, and parse the output using textfsm templates. 
The output will be saved to a file named after the hostname of the device.
The script will also print the output to the console in a tabular format using the tabulate library.  
The script will also print the total execution time of the script.

Only tested on commands listed. Next step to test more commands and custom textfsm templates.
"""


import getpass
from scrapli import Scrapli
from tabulate import tabulate
from datetime import datetime
import time

#get time for execution
start_time = datetime.now()

#open box before eating pizza
with open("devices.txt", "r") as f:
   devices = [line.strip() for line in f if line.strip()]

#get creds
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

#umm....duh
commands = [
    "show cdp neighbors", 
    "show ip int brief"
]

#start loop for each device in devices.txt
for host in devices:
    device = {
        "host": host,
        "auth_username": username,
        "auth_password": password,
        "auth_strict_key": False,
        "platform": "cisco_iosxe"
    }

    #empty string to hold output for each device
    output = ""

    #start scrapli connection
    with Scrapli(**device) as ssh:
        hostname = ssh.get_prompt().rstrip("#").strip()
        print(f"Connected to {hostname}\n")

        #loop through commands and send to device
        for cmd in commands:
            reply = ssh.send_command(cmd)

                # print(f"Output for command '{cmd}':")
                # print(reply.result)

            parsed = reply.textfsm_parse_output()

            if parsed:
                    # print("\nParsed output:")
                    # for row in parsed:
                    #     print(row)
                table = tabulate(parsed, headers="keys", tablefmt="grid")

                print(table)
                output += f"\n{'=' * 60}\n"
                output += f"Host: {hostname}\n"
                output += f"Command: {cmd}\n"
                output += f"{'=' * 60}\n"
                output += table
                output += "\n"

            else:
                print(reply.result)

                output += f"\n{'=' * 60}\n"
                output += f"Host: {hostname}\n"
                output += f"Command: {cmd}\n"
                output += f"{'=' * 60}\n"
                output += reply.result
                output += "\n"
            # print()


        #write output to file named after hostname
        with open(f"{hostname}.txt", "w") as f:
            f.write(output)

#Nice to see. time full script taken.
end_time = (datetime.now() - start_time).total_seconds()
print(f"Total execution time: {end_time:.2f} seconds")

