import socket
import argparse


def scan_port(ip, port, verbose=False):
    """
    Scan a single port on the target IP.
    :param ip: Target IP address.
    :param port: Port number to scan.
    :param verbose: Whether to print detailed output.
    :return: True if the port is open, False otherwise.
    """
    try:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((ip, port))
            if result == 0:
                if verbose:
                    print(f"[+] Port {port}: OPEN")
                return True
            else:
                if verbose:
                    print(f"[-] Port {port}: CLOSED")
                return False
    except Exception as e:
        if verbose:
            print(f"[!] Error scanning port {port}: {e}")
        return False


def scan_ports(ip, ports, verbose=False):
    """
    Scan multiple ports on a given IP address.
    :param ip: Target IP address.
    :param ports: List of ports to scan.
    :param verbose: Whether to print detailed output.
    :return: List of open ports.
    """
    open_ports = []
    print(f"Scanning {ip}...")
    for port in ports:
        if scan_port(ip, port, verbose):
            open_ports.append(port)
    return open_ports


def parse_ports(port_arg):
    """
    Parse the port argument to determine which ports to scan.
    :param port_arg: Argument specifying the ports ('all', 'start-end', or 'port1,port2,...').
    :return: List of ports to scan.
    """
    if port_arg == "all":
        return range(1, 65536)
    elif "-" in port_arg:
        start, end = map(int, port_arg.split("-"))
        return range(start, end + 1)
    else:
        return [int(port) for port in port_arg.split(",")]


def main():

    parser = argparse.ArgumentParser(description="Port Scanner with Verbose Mode")
    parser.add_argument("-t", "--target", help="Target IP address", required=True)
    parser.add_argument(
        "-p",
        "--ports",
        help="Ports to scan ('all', 'start-end', or 'port1,port2,...')",
        required=True,
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    args = parser.parse_args()

    ports = parse_ports(args.ports)

    verbose_mode = args.verbose
    open_ports = scan_ports(args.target, ports, verbose_mode)
    print(f"\nOpen ports on {args.target}: {open_ports}")


if __name__ == "__main__":
    main()
