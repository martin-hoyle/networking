from scrapli import Scrapli
from getpass import getpass

username = input("Username: ")
password = getpass("Password: ")

with open("devices.txt", "r") as f:
   devices = [line.strip() for line in f if line.strip()]

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
        "auth_username": username,
        "auth_password": password,
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