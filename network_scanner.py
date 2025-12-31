"""
Network Scanner for Local Devices
Scans the local network to identify connected devices, including Shark robotic vacuums.
"""

import socket
import subprocess
import re
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Tuple
import ipaddress


def get_local_ip() -> str:
    """Get the local IP address of this machine."""
    try:
        # Create a socket to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("*******", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return "192.168.40.1"  # Default to gateway network


def get_network_range(local_ip: str = None) -> str:
    """Return the configured network range."""
    # Fixed network range for 192.168.40.0/24
    return "192.168.40.0/24"


def ping_host(ip: str) -> Tuple[str, bool]:
    """Ping a single IP address to check if it's alive."""
    try:
        # Windows uses -n for count, Linux/Mac use -c
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', '-w', '1000', ip]
        
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=2
        )
        
        return (ip, result.returncode == 0)
    except Exception:
        return (ip, False)


def get_mac_address(ip: str) -> str:
    """Get MAC address for an IP using ARP."""
    try:
        # Run arp command to get MAC address
        result = subprocess.run(
            ['arp', '-a', ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=2
        )
        
        # Parse MAC address from output
        # Windows format: "  Internet Address      Physical Address      Type"
        output = result.stdout
        mac_match = re.search(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', output)
        
        if mac_match:
            return mac_match.group(0).upper()
        return "Unknown"
    except Exception:
        return "Unknown"


def get_hostname(ip: str) -> str:
    """Try to get hostname for an IP address."""
    try:
        hostname = socket.gethostbyaddr(ip)[0]
        return hostname
    except Exception:
        return "Unknown"


def check_common_ports(ip: str) -> List[int]:
    """Check common ports to identify device type."""
    common_ports = [80, 443, 8080, 8443, 22, 23, 5000]
    open_ports = []
    
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex((ip, port))
            sock.close()
            
            if result == 0:
                open_ports.append(port)
        except Exception:
            pass
    
    return open_ports


def identify_shark_vacuum(ip: str, mac: str, hostname: str, ports: List[int]) -> bool:
    """
    Identify if a device is likely a Shark vacuum based on various indicators.
    """
    indicators = []
    
    # Check hostname for Shark-related keywords
    hostname_lower = hostname.lower()
    shark_keywords = ['shark', 'rvac', 'robot', 'vacuum', 'iq', 'ion']
    
    if any(keyword in hostname_lower for keyword in shark_keywords):
        indicators.append(f"Hostname contains Shark-related keyword: {hostname}")
    
    # Check MAC address vendor (Shark vacuums often use specific manufacturers)
    # Common IoT device manufacturers
    mac_prefix = mac.replace(':', '').replace('-', '')[:6]
    
    # Check for common IoT device ports
    if 8080 in ports or 8443 in ports:
        indicators.append(f"IoT-common ports open: {ports}")
    
    return len(indicators) > 0, indicators


def scan_network(network_range: str, max_workers: int = 50) -> List[Dict]:
    """Scan the network range for active devices."""
    print(f"Scanning network: {network_range}")
    print("This may take a minute or two...\n")
    
    # Generate list of IPs to scan
    network = ipaddress.ip_network(network_range, strict=False)
    ip_list = [str(ip) for ip in network.hosts()]
    
    active_devices = []
    
    # Ping sweep with threading
    print(f"Step 1/3: Pinging {len(ip_list)} addresses...")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_ip = {executor.submit(ping_host, ip): ip for ip in ip_list}
        
        completed = 0
        for future in as_completed(future_to_ip):
            ip, is_alive = future.result()
            completed += 1
            
            if completed % 50 == 0:
                print(f"  Progress: {completed}/{len(ip_list)}")
            
            if is_alive:
                active_devices.append(ip)
    
    print(f"Found {len(active_devices)} active devices\n")
    
    # Get details for each active device
    print("Step 2/3: Gathering device information...")
    devices_info = []
    
    for idx, ip in enumerate(active_devices, 1):
        print(f"  Scanning device {idx}/{len(active_devices)}: {ip}")
        
        mac = get_mac_address(ip)
        hostname = get_hostname(ip)
        ports = check_common_ports(ip)
        
        device_info = {
            'ip': ip,
            'mac': mac,
            'hostname': hostname,
            'open_ports': ports
        }
        
        devices_info.append(device_info)
    
    return devices_info


def main():
    """Main function to run the network scanner."""
    print("=" * 60)
    print("Network Scanner - Shark Vacuum Locator")
    print("=" * 60)
    print()
    
    # Get local network information
    local_ip = get_local_ip()
    network_range = get_network_range(local_ip)
    
    print(f"Your local IP: {local_ip}")
    print(f"Scanning network: {network_range}")
    print()
    
    # Scan the network
    devices = scan_network(network_range)
    
    # Analyze devices
    print("\nStep 3/3: Analyzing devices...")
    print("=" * 60)
    print("Active Devices Found:")
    print("=" * 60)
    
    shark_candidates = []
    
    for device in devices:
        print(f"\nIP Address: {device['ip']}")
        print(f"  MAC Address: {device['mac']}")
        print(f"  Hostname: {device['hostname']}")
        print(f"  Open Ports: {device['open_ports'] if device['open_ports'] else 'None detected'}")
        
        # Check if it might be a Shark vacuum
        is_shark, indicators = identify_shark_vacuum(
            device['ip'],
            device['mac'],
            device['hostname'],
            device['open_ports']
        )
        
        if is_shark:
            print(f"  ⭐ POSSIBLE SHARK VACUUM:")
            for indicator in indicators:
                print(f"     - {indicator}")
            shark_candidates.append(device)
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total devices found: {len(devices)}")
    print(f"Possible Shark vacuums: {len(shark_candidates)}")
    
    if shark_candidates:
        print("\nLikely Shark Vacuum(s):")
        for device in shark_candidates:
            print(f"  • {device['ip']} - {device['hostname']} ({device['mac']})")
    else:
        print("\nNo obvious Shark vacuum detected.")
        print("The vacuum might be:")
        print("  - Using a generic hostname")
        print("  - Currently offline or in sleep mode")
        print("  - On a different network/VLAN")
        print("\nCheck the full device list above for devices with generic names.")


if __name__ == "__main__":
    main()
