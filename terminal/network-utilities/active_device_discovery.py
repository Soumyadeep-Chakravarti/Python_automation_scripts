import scapy.all as scapy
import asyncio
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(
    filename="network_devices.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)
logging.getLogger().addHandler(logging.StreamHandler())


# Device Class to store network device information (IP, MAC)
class Device:
    def __init__(self, ip, mac):
        self.ip = ip
        self.mac = mac

    def __repr__(self):
        return f"Device(IP: {self.ip}, MAC: {self.mac})"


# NetworkScanner Class to encapsulate network scanning functionality
class NetworkScanner:
    def __init__(self, subnet):
        self.subnet = subnet
        self.active_devices = []

    # Function to perform a ping sweep and discover active IPs
    def ping_sweep(self):
        active_ips = []
        for i in range(1, 255):  # Scan 192.168.1.1 to 192.168.1.254
            ip = f"{self.subnet}.{i}"
            response = subprocess.run(
                ["ping", "-c", "1", "-w", "1", ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            if response.returncode == 0:
                active_ips.append(ip)
                logging.info(f"Active IP found: {ip}")
        return active_ips

    # Function to perform an ARP scan and retrieve IP and MAC addresses
    def arp_scan(self, ip_range):
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request

        # Send ARP request and receive response
        devices = scapy.srp(arp_request_broadcast, timeout=2, verbose=False)[0]

        for device in devices:
            self.active_devices.append(Device(device[1].psrc, device[1].hwsrc))
            logging.info(
                f"Device found: IP = {device[1].psrc}, MAC = {device[1].hwsrc}"
            )

    # Function to scan the network (ping and ARP)
    def scan_network(self):
        # Ping Sweep
        loop = asyncio.get_event_loop()
        with ThreadPoolExecutor() as pool:
            active_ips = loop.run_in_executor(pool, self.ping_sweep)
            active_ips = loop.run_until_complete(active_ips)

        # ARP Scan
        ip_range = f"{self.subnet}.1/24"
        with ThreadPoolExecutor() as pool:
            self.arp_scan(ip_range)

    # Method to display results in a readable format
    def display_results(self):
        if not self.active_devices:
            logging.info("No active devices found.")
            print("No active devices found.")
        else:
            logging.info(f"Found {len(self.active_devices)} devices:")
            print(f"Found {len(self.active_devices)} devices:")
            for device in self.active_devices:
                print(f"IP: {device.ip}, MAC: {device.mac}")


# Utility function to automatically detect the subnet
def get_local_subnet():
    # Get the local network interfaces
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            # Check if the address is an IPv4 address
            if addr.family == psutil.AF_INET:
                ip_address = addr.address
                netmask = addrs[1].address  # The netmask is in the second tuple
                # Calculate the subnet using the IP address and netmask
                network = ipaddress.IPv4Network(f"{ip_address}/{netmask}", strict=False)
                return str(
                    network.network_address
                )  # Return the base network address (subnet)
    raise Exception("No valid network interface found.")


# Main function to execute the network scanning process
def main():
    # Automatically detect the subnet
    try:
        subnet = get_local_subnet()
        logging.info(f"Detected local subnet: {subnet}.0/24")
        print(f"Detected local subnet: {subnet}.0/24")
    except Exception as e:
        logging.error(f"Error detecting subnet: {e}")
        print(f"Error detecting subnet: {e}")
        return

    # Initialize the NetworkScanner with the detected subnet
    scanner = NetworkScanner(subnet)

    # Start scanning the network
    scanner.scan_network()

    # Display the results
    scanner.display_results()


if __name__ == "__main__":
    main()
