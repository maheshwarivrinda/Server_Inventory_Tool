# Server Inventory Tool

A Python command-line tool for managing a server inventory. It lets you
add and remove servers, check whether they respond to ping, and export
the inventory as a CSV report. It can be used interactively through a
text menu or non-interactively from the command line, for example in a
bash script or CI/CD pipeline.

## Features

- Store servers with name, address, environment, role, status and
  last-checked time
- Validate environments (`dev`, `test`, `prod`) and prevent duplicate names
- Extra confirmation before removing a `prod` server
- Check one or all servers with `ping`
- Data saved automatically to a JSON file
- Export a timestamped CSV report
- Exit codes suitable for scripts and pipelines

## Data format

Each server is a dictionary:

| Key | Description | Valid values |
|---|---|---|
| `namn` | Server name (unique) | any text |
| `adress` | Hostname or IP address | any text |
| `miljo` | Environment | `dev`, `test`, `prod` |
| `roll` | Role of the server | any text |
| `status` | Result of last check | `up`, `down`, `unknown` |
| `senast_kontrollerad` | Time of last check | `YYYY-MM-DD HH:MM` |


New servers always start with status `unknown`.

## Starting the program

### Mode 1: Text menu

```bash
python3 main.py
```

The menu loops until you choose Quit:

1. Show all servers
2. Show servers in an environment
3. Add a server
4. Remove a server
5. Check one server
6. Check all servers
7. Export report as CSV
8. Quit

### Mode 2: Command line

| Command | What happens |
|---|---|
| `python3 main.py --lista` | Print all servers |
| `python3 main.py --lista --miljo prod` | Print only `prod` servers |
| `python3 main.py --kontrollera web01` | Check the server `web01` |
| `python3 main.py --kontrollera-alla` | Check all servers |
| `python3 main.py --export` | Create a CSV report |
| `python3 main.py --help` | Show help text |

### Exit codes

| Code | Meaning |
|---|---|
| 0 | Everything went well |
| 1 | At least one checked server is down, or the server given to `--kontrollera` does not exist |

Example:

```bash
python3 main.py --kontrollera-alla
echo $?
```

## Environment variable

The data file name is read from `INVENTORY_DATAFIL`. If it is not set,
`servrar.json` is used.

```bash
# Use the default file (servrar.json)
python3 main.py --lista

# Use a different file
INVENTORY_DATAFIL=test.json python3 main.py --lista
```

If the data file does not exist, the program starts with an empty list
and creates the file the first time something is saved.

## CSV reports

Reports are saved in `rapporter/` with the date and time in the file
name, for example `rapporter/inventering_2026-11-18_1337.csv`. The
folder is created automatically. It is listed in `.gitignore`.

## Project structure

```
server_inventory/
├── main.py           # Entry point: argparse, exit codes
├── meny.py           # Text menu and printing of servers
├── modeller.py       # Server data: create, find, add, remove, validation
├── lagring.py        # JSON loading/saving and CSV export
├── kontroller.py     # Ping check and status update
├── servrar.json      # Default data file
├── rapporter/        # Generated CSV reports (git-ignored)
├── .gitignore
├── README.md
└── REDOGORELSE.md
```
