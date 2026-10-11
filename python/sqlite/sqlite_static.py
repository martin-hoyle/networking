import sqlite3
import pandas as pd

conn = sqlite3.connect("database/sh_int.db")

cur = conn.cursor()

sh_int = [
    {'hostname': 'Router-01', 'interface': 'Ethernet0/0', 'ip_address': '192.168.1.11', 'status': 'up', 'proto': 'up'},
    {'hostname': 'Router-01', 'interface': 'Ethernet0/1', 'ip_address': '10.0.0.1', 'status': 'up', 'proto': 'up'},
    {'hostname': 'Router-01', 'interface': 'Ethernet0/2', 'ip_address': 'unassigned', 'status': 'up', 'proto': 'up'},
    {'hostname': 'Router-01', 'interface': 'Ethernet0/3', 'ip_address': 'unassigned', 'status': 'up', 'proto': 'up'},
    {'hostname': 'Router-01', 'interface': 'Loopback0', 'ip_address': '10.255.0.1', 'status': 'up', 'proto': 'up'},
    {'hostname': 'Router-02', 'interface': 'Ethernet0/0', 'ip_address': '192.168.1.12', 'status': 'up', 'proto': 'up'},
    {'hostname': 'Router-02', 'interface': 'Ethernet0/1', 'ip_address': '10.0.0.2', 'status': 'up', 'proto': 'up'},
    {'hostname': 'Router-02', 'interface': 'Ethernet0/2', 'ip_address': 'unassigned', 'status': 'administratively down', 'proto': 'down'},
    {'hostname': 'Router-02', 'interface': 'Ethernet0/3', 'ip_address': 'unassigned', 'status': 'administratively down', 'proto': 'down'},
    {'hostname': 'Router-02', 'interface': 'Loopback0', 'ip_address': '10.255.0.2', 'status': 'up', 'proto': 'up'}
]

df = pd.DataFrame(sh_int)

# Create table if it does not already exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS interfaces (
        hostname TEXT,
        interface TEXT,
        ip_address TEXT,
        status TEXT,
        proto TEXT,
        UNIQUE(hostname, interface)
    )
""")

# Insert new rows or update existing rows
for _, row in df.iterrows():

    cur.execute("""
        INSERT INTO interfaces (hostname, interface, ip_address, status, proto)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(hostname, interface) DO UPDATE SET
            ip_address=excluded.ip_address,
            status=excluded.status,
            proto=excluded.proto
    """, (row['hostname'], row['interface'], row['ip_address'], row['status'], row['proto']))

        
conn.commit()

print("=== DataFrame ===")
print(df)

db = pd.read_sql_query(
    "SELECT * FROM interfaces",
    conn
)

print("\n=== DataFrame read from DB ===")
print(db)

conn.close()