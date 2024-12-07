import socket


def scan_port(ip, port):
    """Scan a single port on the target IP."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)  
            result = s.connect_ex((ip, port))
            if result == 0:
                return True
            return False
    except Exception as e:
        print(f"Error scanning port {port} on {ip}: {e}")
        return False


print(scan_port('127.0.0.1',8000))