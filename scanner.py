import socket
import threading
from concurrent.futures import ThreadPoolExecutor
import sys

def scan_port(target, port):
    """Try to connect to a specific port on the target"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # 1 second timeout per port
        result = sock.connect_ex((target, port))
        sock.close()
        
        if result == 0:
            print(f"Port {port:5d} : OPEN")
            return True
        return False
    except Exception as e:
        return False

def port_scanner(target, ports):
    """Main scanner function - scans multiple ports concurrently"""
    print(f"Scanning {target} for open ports...")
    print("Port     Status")
    print("------------------------")
    
    open_ports = []
    
    # Multi-threaded scanning (100 threads max for speed)
    with ThreadPoolExecutor(max_workers=100) as executor:
        results = executor.map(lambda port: scan_port(target, port), ports)
        open_ports = [port for port, is_open in zip(ports, results) if is_open]
    
    print(f"\nScan complete! Found {len(open_ports)} open ports:")
    for port in sorted(open_ports):
        print(f"  - {port}")
    
    return open_ports

# Common service ports (top ones you see everywhere)
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139,  # FTP, SSH, Telnet, SMTP, DNS, HTTP, POP3, RPC, NetBIOS
    143, 443, 993, 995, 1723, 3306, 3389, 5432,  # IMAP, HTTPS, IMAPS, POP3S, PPTP, MySQL, RDP, PostgreSQL
    5900, 8080, 8443                            # VNC, HTTP-Alt, HTTPS-Alt
]

def main():
    print("Simple Network Port Scanner")
    print("===========================")
    
    target = input("Enter target IP or domain (e.g., 192.168.1.1, scanme.nmap.org): ").strip()
    
    if not target:
        print("No target specified.")
        return
    
    print("\nOptions:")
    print("1. Quick scan (top 25 common ports)")
    print("2. Full scan (ports 1-1000)")
    print("3. Custom port range (e.g., 1-100, 80-443)")
    
    choice = input("Choose option (1/2/3): ").strip()
    
    if choice == "1":
        ports = COMMON_PORTS
        port_scanner(target, ports)
    elif choice == "2":
        ports = range(1, 1001)
        port_scanner(target, ports)
    elif choice == "3":
        range_input = input("Enter port range (e.g., 1-100): ").strip()
        try:
            start, end = map(int, range_input.split('-'))
            ports = range(start, end + 1)
            port_scanner(target, ports)
        except:
            print("Invalid range format. Use: 1-100")
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nScan stopped by user.")
        sys.exit(0)