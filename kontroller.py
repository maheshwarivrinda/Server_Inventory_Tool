import subprocess
from datetime import datetime

def check_server(address):
    """Ping a server once. Return True if it responds."""
    try:
        result = subprocess.run(
                ["ping", "-c", "1", address],
                capture_output=True,
                text=True
                )
        return result.returncode == 0
    except Exception:
        return False

def update_server_status(server):
    if check_server(server["adress"]):
         server["status"] = "up"
    else:
        server["status"] = "down"
     server["senast_kontrollerad"] = datetime.now().strftime("%Y-%m-%d %H:%M")
     return server["status"]


def check_all_servers(servers):
     down_count = 0
     for server in servers:
         print(f"Checking {server['namn']} ({address})...")
         if update_server_status(server) == "down":
             down_count += 1

     return down_count
