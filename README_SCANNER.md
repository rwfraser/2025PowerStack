# Network Scanner - Shark Vacuum Locator

A Python-based network scanner to identify devices on your local network, with special focus on locating Shark robotic vacuums.

## Features

- Scans your entire local subnet (typically 254 addresses)
- Multi-threaded for fast scanning
- Identifies devices by IP, MAC address, hostname, and open ports
- Highlights potential Shark vacuum devices based on naming patterns
- Works on Windows, Linux, and macOS

## Requirements

- Python 3.6 or higher (uses built-in libraries only)
- Administrator/elevated privileges may be needed for some operations

## Usage

Simply run the scanner:

```powershell
python network_scanner.py
```

The scanner will:
1. Detect your local IP and network range
2. Ping all addresses in the subnet
3. Gather detailed information about active devices
4. Identify potential Shark vacuum candidates

## How It Identifies Shark Vacuums

The scanner looks for:
- Hostnames containing keywords like "shark", "rvac", "robot", "vacuum", "iq", "ion"
- Common IoT device ports (8080, 8443)
- Device characteristics typical of smart home devices

## Tips

- Make sure your Shark vacuum is powered on and connected to WiFi
- The vacuum should be on the same network as your computer
- If not detected automatically, check the full device list for generic hostnames
- You can look up MAC addresses online to identify manufacturers
- Some Shark vacuums may use generic hostnames or be in sleep mode

## Manual Checking

If the scanner doesn't automatically identify your vacuum, you can:
1. Check each device's IP address in a web browser (http://IP_ADDRESS)
2. Use the Shark mobile app to check the device's IP address
3. Check your router's admin panel for connected devices

## Common Shark Vacuum Ports

- Port 80/443: Web interface (if available)
- Port 8080/8443: Alternative web/API ports
- Check the Shark app or documentation for your specific model
