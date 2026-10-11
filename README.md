# Networking DevOps Toolkit

A practical collection of Linux setup scripts, Docker configuration, and Python network-automation tools for collecting device output, parsing results, and storing or reporting data.

## Repository layout

```text
.
├── README.md
├── docker/
│   └── mongodb/
│       └── compose.yaml
├── linux/
│   └── bash/
│       ├── redhat-devops-install.sh
│       └── ubuntu-devops-install.sh
└── python/
    ├── first.py
    ├── get.py
    ├── input/
    │   ├── commands.txt
    │   └── devices.txt
    ├── mongodb/
    │   ├── mongodb_fulltable.py
    │   ├── mongo_fulldb.py
    │   ├── mongo_input.py
    │   ├── mongo_ping.py
    │   └── mongo_testdb.py
    ├── output/
    │   ├── network_environment.csv
    │   ├── network_report.xlsx
    │   ├── Router-01.txt
    │   └── Router-02.txt
    ├── pandas/
    │   ├── pandas_csv.py
    │   ├── pandas_xlsx.py
    │   └── pandatest.py
    ├── sqlite/
    │   ├── database/
    │   │   └── sh_int.db
    │   ├── sqlite_base.py
    │   └── sqlite_static.py
    └── textfsm/
        └── textfsm_base.py
```

## Prerequisites

- Linux with Bash
- Python 3.10 or later
- Docker and Docker Compose for MongoDB
- Network reachability and valid credentials for the devices managed by the scripts

## Installation

### Linux DevOps tools

Run the installer matching your distribution:

```bash
# Ubuntu / Debian
bash linux/bash/ubuntu-devops-install.sh

# RHEL / CentOS / Fedora
bash linux/bash/redhat-devops-install.sh
```

### Python environment

```bash
cd python
python3 -m venv .venv
source .venv/bin/activate
pip install scrapli textfsm pandas openpyxl pymongo
```

## MongoDB

Start MongoDB using the provided Compose file:

```bash
docker compose -f docker/mongodb/compose.yaml up -d
```

Stop it with:

```bash
docker compose -f docker/mongodb/compose.yaml down
```

## Usage

1. Add target devices to `python/input/devices.txt`.
2. Add the commands to run against those devices to `python/input/commands.txt`.
3. Run a collection script, for example:

   ```bash
   cd python
   python get.py
   ```

4. Review raw output and generated reports in `python/output/`.

## Components

| Path | Purpose |
|---|---|
| `docker/mongodb/` | Docker Compose configuration for MongoDB |
| `linux/bash/` | Distribution-specific DevOps environment installation scripts |
| `python/input/` | Device inventory and commands to execute |
| `python/output/` | Raw device output, CSV exports, and Excel reports |
| `python/mongodb/` | MongoDB connectivity, ingestion, and test scripts |
| `python/sqlite/` | SQLite examples and local interface database |
| `python/pandas/` | CSV and Excel reporting examples |
| `python/textfsm/` | TextFSM parsing examples for network command output |
| `python/get.py` | Main network-device collection workflow |
| `python/first.py` | Initial Python example or test script |

## Data and outputs

- `python/output/Router-*.txt` contains raw command output collected from devices.
- `python/output/network_environment.csv` and `network_report.xlsx` contain processed reporting data.
- `python/sqlite/database/sh_int.db` is a local SQLite database used by the SQLite examples.

## Housekeeping

Remove generated Python bytecode with:

```bash
find . -type d -name __pycache__ -prune -exec rm -rf {} +
```

Recommended `.gitignore` entries:

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
.env

# Generated outputs and local databases
python/output/*
!python/output/.gitkeep
python/sqlite/database/*.db
```

## Security notes

- Do not commit device usernames, passwords, enable secrets, API keys, or private keys.
- Prefer environment variables, a secrets manager, or an untracked local configuration file.
- Review `devices.txt` and collected output before sharing this repository.
