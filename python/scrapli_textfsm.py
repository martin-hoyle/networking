import getpass
from scrapli import Scrapli
from tabulate import tabulate
from datetime import datetime
import time

start_time = datetime.now()

with open("devices.txt", "r") as f:
   devices = [line.strip() for line in f if line.strip()]


username = input("Enter username: ")
password = getpass.getpass("Enter password: ")


commands = [
    "show cdp neighbors", 
    "show ip int brief"
]

for host in devices:
    device = {
        "host": host,
        "auth_username": username,
        "auth_password": password,
        "auth_strict_key": False,
        "platform": "cisco_iosxe"
    }


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

            else:
                print(reply.result)

                output += f"\n{'=' * 60}\n"
                output += f"Host: {hostname}\n"
                output += f"Command: {cmd}\n"
                output += f"{'=' * 60}\n"
                output += reply.result
                output += "\n"
            # print()



        with open(f"{hostname}.txt", "w") as f:
            f.write(output)

end_time = (datetime.now() - start_time).total_seconds()
print(f"Total execution time: {end_time:.2f} seconds")

