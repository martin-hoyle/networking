import getpass
from scrapli import Scrapli
import pandas as pd
from datetime import datetime

# get time for execution
start_time = datetime.now()

# open devices file
with open("devices.txt", "r") as f:
    devices = [line.strip() for line in f if line.strip()]

# get credentials
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

# commands to run
commands = [
    "show ip int brief",
    "show cdp neighbors",
    "show ip route"
]

# store output for each command
command_output = {}

# start loop for each device
for host in devices:

    device = {
        "host": host,
        "auth_username": username,
        "auth_password": password,
        "auth_strict_key": False,
        "platform": "cisco_iosxe"
    }

    with Scrapli(**device) as ssh:

        hostname = ssh.get_prompt().rstrip("#").strip()
        print(f"Connected to {hostname}\n")

        # loop through commands
        for cmd in commands:

            reply = ssh.send_command(cmd)

            parsed = reply.textfsm_parse_output()

            # add hostname to each record
            parsed = [
                {"hostname": hostname, **interface}
                for interface in parsed
            ]

            # create list for command if it doesn't exist
            if cmd not in command_output:
                command_output[cmd] = []

            # add this device's results
            command_output[cmd].extend(parsed)

# create Excel workbook
with pd.ExcelWriter("output/network_report.xlsx", engine="openpyxl") as writer:

    for cmd, data in command_output.items():

        df = pd.DataFrame(data)

        # Excel sheet names cannot contain certain characters
        sheet_name = cmd.replace("show ", "").replace(" ", "_")[:31]

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        print(f"Created sheet: {sheet_name}")

# execution time
end_time = (datetime.now() - start_time).total_seconds()
print(f"Total execution time: {end_time:.2f} seconds")