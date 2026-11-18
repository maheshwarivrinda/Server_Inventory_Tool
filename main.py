import argparse 
import sys 
import lagring 
import kontroller
import modeller
import meny


def build_parser():
    """Create the argument parser with all supported options."""
    parser = argparse.ArgumentParser(
        description="Server inventory tool. Run without arguments for the text menu."
    )
    parser.add_argument(
        "--lista", action="store_true",
        help="print all servers and exit",
    )
    parser.add_argument(
        "--miljo", choices=modeller.VALID_ENVIRONMENTS,
        help="with --lista: only show servers in this environment",
    )
    parser.add_argument(
        "--kontrollera", metavar="NAMN",
        help="check the server with this name",
    )
    parser.add_argument(
        "--kontrollera-alla", action="store_true",
        help="check all servers",
    )
    parser.add_argument(
        "--export", action="store_true",
        help="export all servers to a CSV report in rapporter/",
    )
    return parser



def main():
    parser = build_parser()
    args = parser.parse_args()
    servers = lagring.load_servers()

    # No arguments at all: start the text menu
    if len(sys.argv) == 1:
        meny.run_menu(servers)
        sys.exit(0)

    exit_code = 0

    if args.lista:
        if args.miljo:
            servers_to_show = [s for s in servers if s["miljo"] == args.miljo]
        else:
            servers_to_show = servers
        meny.print_servers(servers_to_show)

    if args.kontrollera:
        server = modeller.find_server(servers, args.kontrollera)
        if server is None:
            print(f"No server named '{args.kontrollera}'.")
            sys.exit(1)
        status = kontroller.update_server_status(server)
        lagring.save_servers(servers)
        print(f"{server['namn']} is {status}.")
        if status == "down":
            exit_code = 1

    if args.kontrollera_alla:
        down_count = kontroller.check_all_servers(servers)
        lagring.save_servers(servers)
        print(f"Check complete. {down_count} server(s) down.")
        if down_count > 0:
            exit_code = 1

    if args.export:
        print(f"Report exported to {lagring.export_csv(servers)}")

    sys.exit(exit_code)


if __name__ == "__main__":
    main()