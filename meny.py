import lagring
import kontroller
import modeller

def print_servers(servers):
    if not servers:
        print("No servers found.") 
        return

    print(
        f"{'NAME':<15}{'ADDRESS':<20}{'ENV':<8}"
        f"{'ROLE':<20}{'STATUS':<10}{'LAST CHECKED':<18}"

    )
    print("-" * 91)
    for s in servers:
        print(
            f"{s['namn']:<15}{s['adress']:<20}{s['miljo']:<8}"
            f"{s['roll']:<20}{s['status']:<10}{s['senast_kontrollerad']:<18}"
        )

def ask_environment():
    """Ask until the user enters a valid environment (G3)."""
    while True:
        environment = input("Environment (dev/test/prod): ").strip().lower()
        if environment in modeller.VALID_ENVIRONMENTS:
            return environment
        print(f"Invalid environment. Choose one of: "
              f"{', '.join(modeller.VALID_ENVIRONMENTS)}")

def add_server_menu(servers):
    name = input("Name: ").strip()
    address = input("Address: ").strip()
    environment = ask_environment()
    role = input("Role: ").strip()

    new_server = modeller.create_server(name, address, environment, role)
    if modeller.add_server(servers, new_server):
        lagring.save_servers(servers)
        print(f"Server '{name}' added.")
    else:
        print(f"A server named '{name}' already exists.")


def remove_server_menu(servers):
    name = input("Name of server to remove: ").strip()
    server = modeller.find_server(servers, name)
    if server is None:
        print(f"No server named '{name}'.")
        return

    if server["miljo"] == "prod":
        answer = input(f"'{name}' is a PROD server. Type 'yes' to confirm: ")
        if answer.strip().lower() != "yes":
            print("Removal cancelled.")
            return

    modeller.remove_server(servers, name)
    lagring.save_servers(servers)
    print(f"Server '{name}' removed.")

def check_one_menu(servers):
    name = input("Name of server to check: ").strip()
    server = modeller.find_server(servers, name)
    if server is None:
        print(f"No server named '{name}'.")
        return
    status = kontroller.update_server_status(server)
    lagring.save_servers(servers)
    print(f"{name} is {status}.")

def run_menu():
    servers = lagring.load_servers()

    while True:

        print("\n=== SERVER INVENTORY TOOL ===")
        print("1. Show all servers")
        print("2. Show servers in an environment")
        print("3. Add a server")
        print("4. remove a server")
        print("5. Check one server")
        print("6. Check all servers")
        print("7. export report as CSV")
        print("8. Exit")

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            print_servers(servers)
        elif choice == "2":
            environment = ask_environment()
            print_servers([s for s in servers if s["miljo"] == environment])
        elif choice == "3":
            add_server_menu(servers)
        elif choice == "4":
            remove_server_menu(servers)
        elif choice == "5":
            check_one_menu(servers)
        elif choice == "6":
            kontroller.check_all_servers(servers)
            lagring.save_servers(servers)
            print("All servers checked and saved.")
        elif choice == "7":
            print(f"Report exported to {lagring.export_csv(servers)}")
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please choose a number from 1 to 8.")


if __name__ == "__main__":
    run_menu()


