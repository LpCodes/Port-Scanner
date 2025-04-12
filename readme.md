# Advanced Port Scanner

A powerful and efficient Python-based port scanner that supports concurrent scanning, service detection, and customizable scanning options.

## Features

- 🔍 **Concurrent Scanning**: Multi-threaded port scanning for improved performance
- 🎯 **Service Detection**: Automatically detects services running on open ports
- 📊 **Progress Tracking**: Real-time progress display with percentage completion
- 🎨 **Colorized Output**: Color-coded results for better readability
- ⚙️ **Customizable**: Configurable timeout, number of workers, and port ranges
- 📦 **Port Presets**: Predefined port ranges for common services
- 🛡️ **Error Handling**: Robust error handling and input validation

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/port-scanner.git
cd port-scanner
```

2. Install the required dependencies:
```bash
pip install colorama
```

## Usage

Basic usage:
```bash
python app.py -t <target_ip> -p <ports>
```

### Command Line Arguments

| Argument | Description | Example |
|----------|-------------|---------|
| `-t, --target` | Target IP address (required) | `-t 192.168.1.1` |
| `-p, --ports` | Ports to scan (required) | `-p common` |
| `-v, --verbose` | Enable verbose output | `-v` |
| `-w, --workers` | Maximum number of concurrent workers (default: 100) | `-w 200` |
| `-to, --timeout` | Connection timeout in seconds (default: 1.0) | `-to 2.0` |

### Port Range Options

The `-p` argument accepts several formats:

1. **Preset Port Ranges**:
   - `common`: Most commonly used ports (21, 22, 23, 25, 53, 80, 110, 143, 443, 445, 3306, 3389, 5432, 8080)
   - `web`: Web server ports (80, 443, 8080, 8443)
   - `database`: Database server ports (1433, 1521, 3306, 5432, 27017)
   - `mail`: Email server ports (25, 110, 143, 465, 587, 993, 995)
   - `remote`: Remote access ports (22, 23, 3389, 5900)

2. **Custom Range**:
   - `start-end`: Scan ports from start to end (inclusive)
   - Example: `-p 80-100`

3. **Specific Ports**:
   - Comma-separated list of ports
   - Example: `-p 80,443,8080`

4. **All Ports**:
   - `all`: Scan all ports (1-65535)

### Examples

1. Scan common ports on a target:
```bash
python app.py -t 192.168.1.1 -p common
```

2. Scan web ports with verbose output:
```bash
python app.py -t 192.168.1.1 -p web -v
```

3. Scan custom range with more workers and longer timeout:
```bash
python app.py -t 192.168.1.1 -p 80-100 -w 200 -to 2.0
```

4. Scan specific ports:
```bash
python app.py -t 192.168.1.1 -p 80,443,8080
```

## Output Format

The scanner provides color-coded output:

- 🟢 **Green**: Open ports and successful operations
- 🔴 **Red**: Closed ports and errors
- 🟡 **Yellow**: Timeouts and warnings
- 🔵 **Cyan**: Status messages

Example output:
```
Scanning 192.168.1.1...
Total ports to scan: 14
Progress: 100.0% (14/14)

Open ports on 192.168.1.1:
[+] Port 80: OPEN - http
[+] Port 443: OPEN - https
```

## Error Handling

The scanner includes comprehensive error handling for:
- Invalid IP addresses
- Invalid port ranges
- Connection timeouts
- Network errors
- Keyboard interrupts (Ctrl+C)

## Requirements

- Python 3.6 or higher
- colorama package

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Security Note

This tool is intended for legitimate network testing and security assessment purposes only. Always ensure you have proper authorization before scanning any network or system.

