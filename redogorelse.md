# REDOGORELSE.md – Server Inventory Tool

## 1. Three Code Examples Explained

* **Funktion with parameter and return value (`modeller.py` – `find_server`)**: 
`def find_server(servers, name):` accepts the server list and a search name. It loops through the list, checking if `server["namn"] == name`, if matched, it returns the server dictionary directly, otherwise returning `None`.

* ** loop (`kontroller.py` – `check_all_servers`)**: 
`for server in servers` iterates through each server in the list. On each turn, it calls `update_server_status(server)` to ping the host and update its status, counts how many servers are offline, and returns that count.

* **Conditional statement (`meny.py` – `remove_server_menu`)**: `if server["miljo"] == "prod":` 
verifies whether a server belongs to the production environment before removing it. If it is, the code asks for a manual confirmation `"yes"`,. If the user types anything else,`if answer.strip().lower() != "yes":` triggers and returns early, stopping the removal so prod servers aren't deleted by accident.

--- 

## 2. Storing Servers in Memory

A **list** works well here because the list acts as an ordered container that lets us easily add (`.append()`) or remove (`.remove()`) servers. Inside the list, each server is represented as a dictionary, which lets us look up specific attributes by meaningful key names like (e.g., `server["adress"]`). 

All values in the server dictionary are of the **string (`str`)** data type:
* `namn`: `str` (e.g., `"web01"`) 
* `adress`: `str` (e.g., `"example.com"`)
* `miljo`: `str` (e.g., `"prod"`) 
* `roll`: `str` (e.g., `"webbserver"`) 
* `status`: `str` (e.g., `"up"`) 
* `senast_kontrollerad`: `str` (e.g., `"2026-11-18 06:50"`)

--- 

## 3. JSON for Data Storage vs. CSV for Reporting

We save operational data in **JSON** (`servrar.json`) using `json.dump()` and `json.load()` because JSON keeps the nested structure(lists and dictionaries) intact when reading from or writing to disk.. 

We export reports to **CSV** (`rapporter/inventering_...csv`) using `csv.DictWriter` because CSV is a a plain spreadsheet format. this make it easy to open in Excel or Google Sheets for anyone who doesn't use Python.

---

## 4. Modular Structure and File Responsibilities

The application is divided into five modular files adhering to Separation of Concerns:

* **`main.py`**: Handles command-line flags with `argparse` (`build_parser`), launches either the menu or CLI actions, and sets script exit codes with (`sys.exit`). 
* **`meny.py`**: handls the user interface, prints formatted tables to the terminal, and runs the interactive menu loop. 
* **`kontroller.py`**:Pings servers using system commands, updates their status, and records the current timestamp.
* **`modeller.py`**: Manages server data in memory (creating, searching, adding, and removing server dictionaries). 
* **`lagring.py`**: Handles file reading and writing for `servrar.json`, checks environment variables, and exports CSV reports into `rapporter`.

--- 

## 5. Standard Library Modules Used. 

* **`json`** (`lagring.py`): Reads and writes server data to `servrar.json`.
* **`csv`** (`lagring.py`): Creates formatted CSV reports using `csv.DictWriter`.
* **`os`** (`lagring.py`): Reads environment variables (`os.environ.get`) to check for custom data files.
* **`sys`** (`main.py`): Checks arguments (`sys.argv`) and returns exit codes (`sys.exit`).
* **`pathlib` (`Path`)** (`lagring.py`): Manages paths cleanly and creates the `rapporter` directory.
* **`subprocess`** (`kontroller.py`): Runs the system `ping` command (`subprocess.run`).
* **`datetime`** (`kontroller.py`, `lagring.py`): Formats date and time strings using `strftime()`.
* **`argparse`** (`main.py`): Parses terminal flags like `--lista` and `--kontrollera`.


---

## 6. Three Good Coding Practices

* Keeping separate files makes the codebase much easier to read and modify without breaking unrelated code.
* Using `with` blocks in `lagring.py` ensures files close automatically, preventing memory leaks or file corruption if a script crashes.
* Reading `INVENTORY_DATAFIL` with a fallback default in `lagring.py` allows changing the input file path without having to edit Python code.
* 

---

## 7. Sources and Tools Used

* Course presentations slides to understand the core Python concepts and requirements. At the same time I used Ai to help me understand the concept using those presenttion. 
* Various python website to practice Python coding skills and look up standard library functions
* Used Ai to learn and understand git commands for linux, python syntaxs and technical errors(like connecting git hub and pycharm and linux)
* 

