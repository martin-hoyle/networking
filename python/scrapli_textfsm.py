from scrapli import Scrapli
import textfsm

with open("devices.txt", "r") as f:
   devices = [line.strip() for line in f if line.strip()]

# devices = [
#     {
#         "host": "192.168.1.197",
#         "auth_username": "cisco",
#         "auth_password": "Cisco123",
#         "auth_strict_key": False,
#         "platform": "cisco_iosxe",
#     }
# ]


commands = [
    "show cdp neighbors", 
    "show ip int brief"
]

for device in devices:

    with Scrapli(**device) as ssh:
        for cmd in commands:
            hostname = (ssh.get_prompt().rstrip("#"))
            print(f"Connected to {hostname}")

            reply = ssh.send_command(cmd)
            print(f"Output for command '{cmd}':\n{reply.result}\n")


            reply = ssh.send_command(cmd)
            parsed = reply.textfsm_parse_output()

            print(reply.result)

            for line in parsed:
                print(line)
