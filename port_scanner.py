"""
Port Scanner - Comprehensive Protocol and Port Discovery
Scans a single IP address for common protocols and ports.
"""

import socket
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
import subprocess
import platform
import time


# Common ports and their services
COMMON_PORTS = {
    # Web Services
    80: "HTTP",
    443: "HTTPS",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    8000: "HTTP-Dev",
    3000: "HTTP-Dev (Node/React)",
    4200: "HTTP-Dev (Angular)",
    5000: "HTTP-Dev (Flask)",
    
    # File Transfer
    20: "FTP-Data",
    21: "FTP-Control",
    22: "SSH/SFTP",
    69: "TFTP",
    115: "SFTP",
    
    # Email
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    465: "SMTPS",
    587: "SMTP-Submission",
    993: "IMAPS",
    995: "POP3S",
    
    # Remote Access
    23: "Telnet",
    3389: "RDP (Remote Desktop)",
    5900: "VNC",
    5901: "VNC-1",
    
    # Database
    1433: "MS SQL Server",
    1521: "Oracle DB",
    3306: "MySQL/MariaDB",
    5432: "PostgreSQL",
    6379: "Redis",
    27017: "MongoDB",
    
    # Network Services
    53: "DNS",
    67: "DHCP-Server",
    68: "DHCP-Client",
    123: "NTP",
    161: "SNMP",
    162: "SNMP-Trap",
    389: "LDAP",
    636: "LDAPS",
    
    # File Sharing
    139: "NetBIOS",
    445: "SMB/CIFS",
    548: "AFP",
    2049: "NFS",
    
    # Messaging/Communication
    1883: "MQTT",
    5222: "XMPP",
    5269: "XMPP-Server",
    6667: "IRC",
    
    # Media Streaming
    554: "RTSP",
    1935: "RTMP",
    8554: "RTSP-Alt",
    
    # IoT/Smart Home
    1900: "UPnP/SSDP",
    5353: "mDNS",
    8883: "MQTT-SSL",
    
    # Proxy/VPN
    1080: "SOCKS Proxy",
    3128: "Squid Proxy",
    8888: "HTTP Proxy",
    1194: "OpenVPN",
    
    # Application Servers
    8009: "Apache Tomcat AJP",
    8081: "HTTP-Alt",
    9000: "HTTP-Alt",
    9090: "HTTP-Alt",
    
    # Monitoring/Management
    9100: "Printer (JetDirect)",
    10000: "Webmin",
    
    # Game Servers
    25565: "Minecraft",
    27015: "Steam/Source Games",
    
    # Docker/Container
    2375: "Docker (unencrypted)",
    2376: "Docker (TLS)",
    
    # Elasticsearch
    9200: "Elasticsearch HTTP",
    9300: "Elasticsearch Transport",
}


def check_ping(ip: str) -> bool:
    """Check if the host is reachable via ping."""
    try:
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-w', '1000', ip]
        
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=3
        )
        
        return result.returncode == 0
    except Exception:
        return False


def scan_port(ip: str, port: int, timeout: float = 1.0) -> Tuple[int, bool, str]:
    """
    Scan a single port on the target IP.
    Returns (port, is_open, service_name)
    """
    service_name = COMMON_PORTS.get(port, "Unknown")
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((ip, port))
        sock.close()
        
        is_open = (result == 0)
        return (port, is_open, service_name)
    except socket.error:
        return (port, False, service_name)
    except Exception:
        return (port, False, service_name)


def grab_banner(ip: str, port: int, timeout: float = 2.0) -> str:
    """
    Attempt to grab a banner from an open port to identify the service.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        sock.connect((ip, port))
        
        # Try to receive banner
        try:
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            return banner if banner else "No banner"
        except:
            # Some services need a request first (like HTTP)
            if port in [80, 8080, 8000, 3000]:
                sock.send(b"GET / HTTP/1.0\r\n\r\n")
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                sock.close()
                return banner[:100] if banner else "No response"
            sock.close()
            return "No banner"
    except Exception as e:
        return "Unable to connect"


def get_hostname(ip: str) -> str:
    """Try to resolve hostname for the IP."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except Exception:
        return "Unable to resolve"


def scan_all_ports(ip: str, max_workers: int = 100) -> List[Dict]:
    """
    Scan all common ports on the target IP.
    """
    print(f"\nScanning {len(COMMON_PORTS)} common ports on {ip}...")
    print("This may take a minute...\n")
    
    open_ports = []
    ports_to_scan = sorted(COMMON_PORTS.keys())
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {
            executor.submit(scan_port, ip, port): port 
            for port in ports_to_scan
        }
        
        completed = 0
        for future in as_completed(future_to_port):
            port, is_open, service_name = future.result()
            completed += 1
            
            if completed % 20 == 0:
                print(f"Progress: {completed}/{len(ports_to_scan)} ports scanned...")
            
            if is_open:
                open_ports.append({
                    'port': port,
                    'service': service_name,
                    'state': 'OPEN'
                })
    
    return sorted(open_ports, key=lambda x: x['port'])


def scan_port_range(ip: str, start_port: int, end_port: int, max_workers: int = 100) -> List[Dict]:
    """
    Scan a range of ports on the target IP.
    """
    print(f"\nScanning ports {start_port}-{end_port} on {ip}...")
    print("This may take several minutes...\n")
    
    open_ports = []
    ports_to_scan = range(start_port, end_port + 1)
    total_ports = end_port - start_port + 1
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_port = {
            executor.submit(scan_port, ip, port): port 
            for port in ports_to_scan
        }
        
        completed = 0
        for future in as_completed(future_to_port):
            port, is_open, service_name = future.result()
            completed += 1
            
            if completed % 100 == 0:
                print(f"Progress: {completed}/{total_ports} ports scanned...")
            
            if is_open:
                open_ports.append({
                    'port': port,
                    'service': service_name if service_name != "Unknown" else f"Port {port}",
                    'state': 'OPEN'
                })
    
    return sorted(open_ports, key=lambda x: x['port'])


def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description='Comprehensive port scanner for a single IP address',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python port_scanner.py 192.168.1.100
  python port_scanner.py 192.168.1.100 --range 1-1000
  python port_scanner.py 192.168.1.100 --banner
        """
    )
    
    parser.add_argument('ip', help='Target IP address to scan')
    parser.add_argument('--range', '-r', help='Port range to scan (e.g., 1-1000). If not specified, scans common ports only.')
    parser.add_argument('--banner', '-b', action='store_true', help='Attempt to grab banners from open ports')
    parser.add_argument('--timeout', '-t', type=float, default=1.0, help='Timeout for each port scan in seconds (default: 1.0)')
    
    args = parser.parse_args()
    
    target_ip = args.ip
    
    # Validate IP address
    try:
        socket.inet_aton(target_ip)
    except socket.error:
        print(f"Error: '{target_ip}' is not a valid IP address")
        sys.exit(1)
    
    print("=" * 70)
    print(f"Port Scanner - Target: {target_ip}")
    print("=" * 70)
    
    # Check if host is up
    print(f"\nChecking if host is reachable...")
    if check_ping(target_ip):
        print(f"✓ Host {target_ip} is UP")
    else:
        print(f"⚠ Host {target_ip} appears DOWN (no ping response)")
        print("  Continuing scan anyway (some hosts block ping)...\n")
    
    # Get hostname
    print(f"\nResolving hostname...")
    hostname = get_hostname(target_ip)
    print(f"Hostname: {hostname}")
    
    # Scan ports
    start_time = time.time()
    
    if args.range:
        # Parse range
        try:
            start_port, end_port = map(int, args.range.split('-'))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                print("Error: Invalid port range. Must be 1-65535 and start <= end")
                sys.exit(1)
            open_ports = scan_port_range(target_ip, start_port, end_port)
        except ValueError:
            print("Error: Invalid range format. Use: START-END (e.g., 1-1000)")
            sys.exit(1)
    else:
        # Scan common ports
        open_ports = scan_all_ports(target_ip)
    
    scan_duration = time.time() - start_time
    
    # Display results
    print("\n" + "=" * 70)
    print("SCAN RESULTS")
    print("=" * 70)
    
    if open_ports:
        print(f"\nFound {len(open_ports)} open port(s):\n")
        print(f"{'PORT':<10} {'STATE':<10} {'SERVICE':<30}")
        print("-" * 70)
        
        for port_info in open_ports:
            print(f"{port_info['port']:<10} {port_info['state']:<10} {port_info['service']:<30}")
        
        # Banner grabbing
        if args.banner and open_ports:
            print("\n" + "=" * 70)
            print("BANNER GRABBING")
            print("=" * 70)
            print("\nAttempting to identify services...\n")
            
            for port_info in open_ports:
                port = port_info['port']
                print(f"Port {port} ({port_info['service']}):")
                banner = grab_banner(target_ip, port)
                if banner and banner != "No banner":
                    print(f"  {banner[:150]}")
                else:
                    print(f"  {banner}")
                print()
    else:
        print("\nNo open ports found.")
        print("This could mean:")
        print("  - The host is not running any services on scanned ports")
        print("  - A firewall is blocking the connection")
        print("  - The host is actually down")
    
    # Summary
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Target: {target_ip}")
    print(f"Hostname: {hostname}")
    print(f"Open ports: {len(open_ports)}")
    print(f"Scan duration: {scan_duration:.2f} seconds")
    print("=" * 70)


if __name__ == "__main__":
    main()
