from scrapli import Scrapli

device = {
    "host": "192.168.1.197",
    "auth_username": "cisco",
    "auth_password": "Cisco123",
    "auth_strict_key": False,
    "platform": "cisco_iosxe",
}

with Scrapli(**device) as conn:
    response = conn.send_command("show version")
    print(response.result)