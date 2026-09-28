from scrapli import Scrapli
from getpass import getpass

#username = input("Username: ")
#password = getpass("Password: ")

with open("../devices/devices.txt", "r") as f:
   devices = [line.strip() for line in f if line.strip()]

# devices = [
#    "192.167.1.197",
#    "192.167.1.232",
#    "192.167.1.115"
# ]

commands = [
    "show version", 
    "show ip int brief", 
    "show run"
    ] 

for host in devices:

    print(f"\n{'=' * 60}")
    print(f"Connecting to {host}")
    print(f"{'=' * 60}")
    
    device = {
        "host": host,
        "auth_username": "cisco",
        "auth_password": "Cisco123",
        "auth_strict_key": False,
        "platform": "cisco_iosxe",
}

    output = ""

    with Scrapli(**device) as conn:
        for cmd in commands:
            response = conn.send_command(cmd)
            print(f"Output for command '{cmd}':\n{response.result}\n")
            
            output += f"\n{'=' * 60}\n"
            output += f"COMMAND: {cmd}\n"
            output += f"{'=' * 60}\n"
            output += response.result
            output += "\n"

    with open(f"{host}.txt", "w") as f:
        f.write(output)