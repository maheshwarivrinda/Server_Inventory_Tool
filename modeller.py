VALID_ENVIRONMENTS = ["dev", "test", "prod"]
VALID_STATUSES = ["up", "down", "unknown"]


def create_server(name, address, environment, role):
    """Return a new server dictionary. New servers always start as unknown."""
    return {
        "namn": name,
        "adress": address,
        "miljo": environment,
        "roll": role,
        "status": "unknown",
        "senast_kontrollerad": "",
    }


def find_server(servers, name):
    """Return the server with this name, or None if it doesn't exist."""
    for server in servers:
        if server["namn"] == name:
            return server
    return None


def add_server(servers, new_server):
    """Add a server unless the name is taken. Return True if added."""
    if find_server(servers, new_server["namn"]) is not None:
        return False
    servers.append(new_server)
    return True


def remove_server(servers, name):
    """Remove a server by name. Return True if it existed."""
    server = find_server(servers, name)
    if server is None:
        return False
    servers.remove(server)
    return True