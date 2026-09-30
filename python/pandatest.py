import pandas as pd

data = [
    {'interface': 'Ethernet0/0', 'ip_address': '192.168.1.11', 'status': 'up', 'proto': 'up'},
    {'interface': 'Ethernet0/1', 'ip_address': '10.0.0.1', 'status': 'up', 'proto': 'up'},
    {'interface': 'Ethernet0/2', 'ip_address': 'unassigned', 'status': 'up', 'proto': 'up'},
    {'interface': 'Ethernet0/3', 'ip_address': 'unassigned', 'status': 'up', 'proto': 'up'},
    {'interface': 'Loopback0', 'ip_address': '10.255.0.1', 'status': 'up', 'proto': 'up'}
]


df = pd.DataFrame(data, index=[0, 1, 2, 3, 4], columns=['interface', 'ip_address', 'status', 'proto'])

df.to_csv('interfaces.csv', index=False)

print(df)

