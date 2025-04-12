# Import necessary libraries
import socket  # For network connections
import argparse  # For command-line argument parsing
import concurrent.futures  # For parallel processing
import time  # For timing operations
from typing import List, Dict  # For type hints
import sys  # For system-specific operations
from colorama import init, Fore, Style  # For colored terminal output

# Initialize colorama for colored output
init()

# Define common port ranges for different services
# These are frequently used ports that we can scan quickly
COMMON_PORTS = {
    "common": [21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080],
    "web": [80, 443, 8080, 8443],
    "database": [1433, 1521, 3306, 5432, 27017],
    "mail": [25, 110, 143, 465, 587, 993, 995],
    "remote": [22, 23, 3389, 5900]
}

def get_service_name(port: int) -> str:
    """
    Try to identify the service running on a given port.
    This function uses the system's service database to find the service name.
    
    Args:
        port (int): The port number to look up
        
    Returns:
        str: The name of the service or 'unknown' if not found
    """
    try:
        return socket.getservbyport(port)
    except:
        return "unknown"

def scan_port(ip: str, port: int, timeout: float = 1.0, verbose: bool = False) -> Dict:
    """
    Scan a single port on the target IP address.
    This function tries to establish a TCP connection to the specified port.
    
    Args:
        ip (str): Target IP address to scan
        port (int): Port number to check
        timeout (float): How long to wait for a response (in seconds)
        verbose (bool): Whether to print detailed information
        
    Returns:
        Dict: A dictionary containing port information and scan results
    """
    # Initialize the result dictionary with default values
    result = {
        "port": port,
        "status": "closed",  # Default status is closed
        "service": None  # Service name will be determined if port is open
    }
    
    try:
        # Create a new socket for the connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            # Set the timeout for the connection attempt
            s.settimeout(timeout)
            
            # Try to connect to the port
            # connect_ex returns 0 if successful, error code otherwise
            result_code = s.connect_ex((ip, port))
            
            if result_code == 0:
                # Port is open
                result["status"] = "open"
                result["service"] = get_service_name(port)
                if verbose:
                    print(f"{Fore.GREEN}[+] Port {port}: OPEN - {result['service']}{Style.RESET_ALL}")
            elif verbose:
                # Port is closed
                print(f"{Fore.RED}[-] Port {port}: CLOSED{Style.RESET_ALL}")
                
    except socket.timeout:
        # Connection attempt timed out
        if verbose:
            print(f"{Fore.YELLOW}[!] Port {port}: TIMEOUT{Style.RESET_ALL}")
    except Exception as e:
        # Handle any other errors
        if verbose:
            print(f"{Fore.YELLOW}[!] Error scanning port {port}: {str(e)}{Style.RESET_ALL}")
    
    return result

def scan_ports(ip: str, ports: List[int], max_workers: int = 100, timeout: float = 1.0, verbose: bool = False) -> List[Dict]:
    """
    Scan multiple ports on a target IP address using multiple threads.
    This function uses ThreadPoolExecutor to scan ports concurrently.
    
    Args:
        ip (str): Target IP address
        ports (List[int]): List of ports to scan
        max_workers (int): Maximum number of concurrent threads
        timeout (float): Connection timeout in seconds
        verbose (bool): Whether to print detailed information
        
    Returns:
        List[Dict]: List of scan results for open ports
    """
    open_ports = []  # Store results for open ports
    total_ports = len(ports)  # Total number of ports to scan
    scanned_ports = 0  # Counter for progress tracking
    
    # Print scan information
    print(f"\n{Fore.CYAN}Scanning {ip}...{Style.RESET_ALL}")
    print(f"Total ports to scan: {total_ports}")
    
    # Create a thread pool for concurrent scanning
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all port scans to the thread pool
        future_to_port = {
            executor.submit(scan_port, ip, port, timeout, verbose): port 
            for port in ports
        }
        
        # Process results as they complete
        for future in concurrent.futures.as_completed(future_to_port):
            scanned_ports += 1
            result = future.result()
            
            # If port is open, add it to the results
            if result["status"] == "open":
                open_ports.append(result)
            
            # Update and display progress
            progress = (scanned_ports / total_ports) * 100
            sys.stdout.write(f"\rProgress: {progress:.1f}% ({scanned_ports}/{total_ports})")
            sys.stdout.flush()
    
    print("\n")
    return open_ports

def parse_ports(port_arg: str) -> List[int]:
    """
    Parse the port argument to determine which ports to scan.
    This function handles different port specification formats.
    
    Args:
        port_arg (str): Port specification string
        
    Returns:
        List[int]: List of ports to scan
        
    Raises:
        ValueError: If port range is invalid
    """
    # Check if the argument matches a predefined port range
    if port_arg in COMMON_PORTS:
        return COMMON_PORTS[port_arg]
    # Check if scanning all ports
    elif port_arg == "all":
        return list(range(1, 65536))
    # Check if it's a port range (e.g., "80-100")
    elif "-" in port_arg:
        start, end = map(int, port_arg.split("-"))
        # Validate port range
        if not (1 <= start <= end <= 65535):
            raise ValueError("Port range must be between 1 and 65535")
        return list(range(start, end + 1))
    # Handle comma-separated list of ports
    else:
        ports = [int(port) for port in port_arg.split(",")]
        # Validate each port
        if not all(1 <= port <= 65535 for port in ports):
            raise ValueError("Ports must be between 1 and 65535")
        return ports

def validate_ip(ip: str) -> bool:
    """
    Check if the given string is a valid IP address.
    
    Args:
        ip (str): IP address to validate
        
    Returns:
        bool: True if valid IP, False otherwise
    """
    try:
        socket.inet_aton(ip)
        return True
    except socket.error:
        return False

def main():
    """
    Main function that handles command-line arguments and orchestrates the scanning process.
    """
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description="Advanced Port Scanner")
    
    # Define command-line arguments
    parser.add_argument("-t", "--target", help="Target IP address", required=True)
    parser.add_argument(
        "-p", "--ports",
        help="Ports to scan (presets: common, web, database, mail, remote; or 'all', 'start-end', or 'port1,port2,...')",
        required=True
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument("-w", "--workers", type=int, default=100, help="Maximum number of concurrent workers")
    parser.add_argument("-to", "--timeout", type=float, default=1.0, help="Connection timeout in seconds")
    
    # Parse command-line arguments
    args = parser.parse_args()

    # Validate IP address
    if not validate_ip(args.target):
        print(f"{Fore.RED}Error: Invalid IP address format{Style.RESET_ALL}")
        return

    try:
        # Parse ports and start scanning
        ports = parse_ports(args.ports)
        open_ports = scan_ports(args.target, ports, args.workers, args.timeout, args.verbose)
        
        # Display results
        if open_ports:
            print(f"\n{Fore.GREEN}Open ports on {args.target}:{Style.RESET_ALL}")
            for port_info in open_ports:
                print(f"{Fore.GREEN}[+] Port {port_info['port']}: OPEN - {port_info['service']}{Style.RESET_ALL}")
        else:
            print(f"\n{Fore.YELLOW}No open ports found on {args.target}{Style.RESET_ALL}")
            
    except ValueError as e:
        # Handle invalid port specifications
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        # Handle user interruption (Ctrl+C)
        print(f"\n{Fore.YELLOW}Scan interrupted by user{Style.RESET_ALL}")
    except Exception as e:
        # Handle any other errors
        print(f"{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")

# Run the main function if the script is executed directly
if __name__ == "__main__":
    main()
