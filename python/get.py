from scrapli import Scrapli
from getpass import getpass

username = getpass("Enter username: ")
password = getpass("Enter password: ")

device = {
    "host": "192.168.1.197",
    "auth_username": username,
    "auth_password": password,
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
}

with Scrapli(**device) as conn:
    response = conn.send_command("show version")
    print(response.result)