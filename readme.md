

# Basic Port Scanner with Verbose Mode

This Python script is a simple port scanner that can scan all ports, a specific range of ports, or specific ports on a target IP address. It also includes a **verbose mode** that provides detailed output for each port scanned.

## Features
- Scan all ports (1–65535).
- Scan a range of ports (e.g., 20–80).
- Scan specific ports (e.g., 22, 80, 443).
- **Verbose output** to show detailed status for each port scanned.
- Works on both Linux and Windows.

---

## Prerequisites

Before using the script, make sure you have **Python 3.x** installed on your system. You will also need to install the `socket` and `argparse` libraries, which are part of the standard Python library, so no additional installation is necessary.

---

## Installation

1. **Download the script**: Save the script as `app.py`.

2. **Make the script executable** (Optional, for Linux/Mac):
   ```bash
   chmod +x app.py
   ```

---

## Usage

You can use this script via the command line or terminal. The basic syntax is as follows:

```bash
python app.py -t <target_ip> -p <ports> [options]
```

### Arguments:
- `-t, --target` (required): **Target IP address** to scan.
- `-p, --ports` (required): **Ports to scan**. You can specify:
  - `all`: Scan all 65,535 ports.
  - `start-end`: Scan a range of ports (e.g., `20-80`).
  - `port1,port2,...`: Scan specific ports (e.g., `22,80,443`).

### Optional Flags:
- `-v, --verbose`: Enable **verbose output** for detailed scanning information (e.g., connection attempts, errors).

---

## Example Commands

### 1. **Scan All Ports with Verbose Output**
This command will scan all ports (1-65535) on the target IP `192.168.1.1` and print detailed messages for each port.

```bash
python app.py -t 192.168.1.1 -p all -v
```

#### Output:
```
Scanning 192.168.1.1...
[-] Port 1: CLOSED
[-] Port 2: CLOSED
[+] Port 22: OPEN
[+] Port 80: OPEN
...
Open ports on 192.168.1.1: [22, 80, 443]
```

### 2. **Scan a Specific Range of Ports with Verbose Output**
This command will scan ports from `20` to `80` on the target IP `192.168.1.1` and print detailed messages.

```bash
python app.py -t 192.168.1.1 -p 20-80 -v
```

#### Output:
```
Scanning 192.168.1.1...
[-] Port 20: CLOSED
[+] Port 22: OPEN
[+] Port 80: OPEN
...
Open ports on 192.168.1.1: [22, 80]
```

### 3. **Scan Specific Ports without Verbose Output**
This command will scan only ports `22`, `80`, and `443` on the target IP `192.168.1.1` and print only the list of open ports (no verbose output).

```bash
python app.py -t 192.168.1.1 -p 22,80,443
```

#### Output:
```
Scanning 192.168.1.1...
Open ports on 192.168.1.1: [22, 80, 443]
```

---

## How It Works

- **Port Scanning**: The script attempts to create a TCP connection to the specified ports on the target IP address. If the connection succeeds, the port is marked as **open**; otherwise, it is **closed**.
- **Verbose Mode**: In verbose mode (`-v`), the script prints the status for each port being scanned (e.g., `OPEN`, `CLOSED`, or errors).

---

