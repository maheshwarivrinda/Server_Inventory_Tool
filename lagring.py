import json 
import csv
import os
from datetime import datetime
from pathlib import Path

REPORT_DIR = "rapporter"
CSV_FIELDS = ["namn", "adress", "miljo", "roll", "status", "senast_kontrollerad"]

def get_data_file():
    return os.environ.get("INVENTORY_DATAFIL", "servrar.json")

def load_servers(filename= DEFAULT_DATA_FILE):
    filepath = Path(filename or get_data_file())
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)

def save_servers(servers, filename=None):
    """Saves the server list back to a JSON file"""
    filepath = Path(filename or get_data_file())
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(servers, file, indent=2, ensure_ascii=False)

def export_csv(servers, output_file="report.csv"):
    """Export all servers to a timestamped CSV file and return the file path."""
    report_dir = Path(REPORT_DIR)
    report_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filepath = report_dir / f"inventering_{timestamp}.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=CSV_files)
        writer.writeheader()
        writer.writerows(servers)
    return filepath