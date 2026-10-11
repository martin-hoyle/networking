import getpass
from scrapli import Scrapli
import pandas as pd
from datetime import datetime

#get time for execution
start_time = datetime.now()

#open box before eating pizza
with open("input/devices.txt", "r") as f:
   devices = [line.strip() for line in f if line.strip()]

with open("input/commands.txt", "r") as f:
    commands = [line.strip() for line in f if line.strip()]

#get creds
username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

#umm....duh
# commands = [
#     "show ip int brief"
# ]


all_output = []

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

            # add hostname to every parsed interface
            for interface in parsed: 
                interface["hostname"] = hostname

            # add this device's data to the master list
            all_output.extend(parsed)
            # print(parsed)

df = pd.DataFrame(all_output, columns=['hostname', 'interface', 'ip_address', 'status', 'proto'])

df.to_csv('output/network_environment.csv', index=False)
# df.to_excel('output/network_environment.xlsx', index=False)

print(df)

#Nice to see. time full script taken.
end_time = (datetime.now() - start_time).total_seconds()
print(f"Total execution time: {end_time:.2f} seconds")