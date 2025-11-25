"""
Creating a Netwrok Scanner so that its able to discover devices connected to the network.
using ping sweep and Port scan by TCP connect method.
"""

import sys
import platform
import subprocess
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import csv
import ipaddress

PING_WORKERS = 100
PORT_SCANNER_WORKERS = 200
PING_TIMEOUT_SEC = 1
CONNECT_TIMEOUT_SEC = 0.5
COMMON_PORTS = [21, 22, 23, 25, 53, 80, 110, 139, 143, 443, 445, 3389]

def ping_host(ip:str)->bool:
    """
    Ping a host to check if it's alive.
    """
    if platform.system().lower() == 'windows':
        param = '-n'
        timeout_param = '-w'
        timeout = str(PING_TIMEOUT_SEC * 1000)  # milliseconds
    else:
        param = '-c'
        timeout_param = '-W'
        timeout = str(PING_TIMEOUT_SEC)  # seconds
    command = ['ping', param, '1', timeout_param, timeout, str(ip)]
    try:
        output = subprocess.check_output(command, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False
    
def scan_ports(ip:str, ports:list)->list:
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(CONNECT_TIMEOUT_SEC)
            result = sock.connect_ex((ip, port))
            if result == 0:
                open_ports.append(port)
    return open_ports   

def discover_devices(subnet:str)->list:
    """
    Discover devices in the given subnet using ping sweep.
    """
    alive_hosts = []
    with ThreadPoolExecutor(max_workers=PING_WORKERS) as executor:
        futures = {executor.submit(ping_host, str(ip)): str(ip) for ip in ipaddress.ip_network(subnet).hosts()}
        for future in as_completed(futures):
            ip = futures[future]
            try:
                if future.result():
                    alive_hosts.append(ip)
            except Exception as e:
                print(f"Error pinging {ip}: {e}")
    return alive_hosts

def main():
    print("Script started")  # Debug print
    if len(sys.argv) != 2:
        print("No subnet argument provided. Using default: 127.0.0.1/32")
        subnet = "127.0.0.1/32"
    else:
        subnet = sys.argv[1]
    print(f"Starting network scan on subnet: {subnet}")
    start_time = datetime.now()
    
    print("Discovering devices...")  # Debug print
    alive_hosts = discover_devices(subnet)
    print(f"Discovered {len(alive_hosts)} alive hosts.")
    
    results = []
    print("Scanning ports...")  # Debug print
    with ThreadPoolExecutor(max_workers=PORT_SCANNER_WORKERS) as executor:
        futures = {executor.submit(scan_ports, ip, COMMON_PORTS): ip for ip in alive_hosts}
        for future in as_completed(futures):
            ip = futures[future]
            try:
                open_ports = future.result()
                results.append((ip, open_ports))
                print(f"{ip}: Open ports: {open_ports}")
            except Exception as e:
                print(f"Error scanning ports on {ip}: {e}")
    
    end_time = datetime.now()
    duration = end_time - start_time
    print(f"Scan completed in {duration}.")
    
    print("Writing results to CSV...")  # Debug print
    with open('network_scan_results.csv', 'w', newline='') as csvfile:
        fieldnames = ['IP Address', 'Open Ports']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for ip, ports in results:
            writer.writerow({'IP Address': ip, 'Open Ports': ', '.join(map(str, ports))})
    
    print("Results saved to network_scan_results.csv")

if __name__ == "__main__":
    main()