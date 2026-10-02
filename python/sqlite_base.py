import sqlite3
import pandas as pd
import datetime

con = sqlite3.connect("database/network_devices.db")


cur = con.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS devices
               (hostname TEXT, 
               ip_address TEXT
               )''')

cur.execute('''CREATE TABLE IF NOT EXISTS neighbors
               (hostname1 TEXT, 
               hostname2 TEXT
               )''')

devices = [
    ("router-01", "192.168.1.11"),
    ("router-02", "192.168.1.12")
]

cur.executemany("INSERT INTO devices (hostname, ip_address) VALUES (?, ?)", devices)

# cur.execute("INSERT INTO devices (hostname, ip_address) VALUES (?, ?)", ("router-01", "192.168.1.11"))
cur.execute("INSERT INTO neighbors (hostname1, hostname2) VALUES (?, ?)", ("router-01", "router-02"))

for row in cur.execute("SELECT * FROM devices"):
    print(row)

for row in cur.execute("SELECT * FROM neighbors"):
    print(row)

con.commit()
con.close()


