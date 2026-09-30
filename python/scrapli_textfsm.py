import getpass
from scrapli import Scrapli
from tabulate import tabulate

# with open("devices.txt", "r") as f:
#    devices = [line.strip() for line in f if line.strip()]


username = input("Enter username: ")
password = getpass.getpass("Enter password: ")

device = {
    "host": "192.168.1.197",
    "auth_username": username,
    "auth_password": password,
    "auth_strict_key": False,
    "platform": "cisco_iosxe"
}



commands = [
    "show cdp neighbors", 
    "show ip int brief"
]
output = ""

with Scrapli(**device) as ssh:
    hostname = ssh.get_prompt().rstrip("#").strip()
    print(f"Connected to {hostname}\n")

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

        print()

with open(f"{hostname}.txt", "w") as f:
    f.write(output)