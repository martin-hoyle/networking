from scrapli import Scrapli
from tabulate import tabulate

# with open("devices.txt", "r") as f:
#    devices = [line.strip() for line in f if line.strip()]

device = {
    "host": "192.168.1.197",
    "auth_username": "cisco",
    "auth_password": "Cisco123",
    "auth_strict_key": False,
    "platform": "cisco_iosxe"
}



commands = [
    "show cdp neighbors", 
    "show ip int brief",
    "show ip ospf neighbor"
]

with Scrapli(**device) as ssh:
    hostname = ssh.get_prompt().rstrip("#").strip()
    print(f"Connected to {hostname}\n")

    for cmd in commands:
        reply = ssh.send_command(cmd)

        print(f"Output for command '{cmd}':")
        print(reply.result)

        parsed = reply.textfsm_parse_output()

        if parsed:
            print("\nParsed output:")
            for row in parsed:
                print(row)
            print(tabulate(parsed, headers="keys", tablefmt="grid"))

        print()
