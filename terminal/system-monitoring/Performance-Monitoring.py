import psutil
import time
from datetime import datetime

# Thresholds for alerts
CPU_THRESHOLD = 80  # in percentage
MEMORY_THRESHOLD = 80  # in percentage
DISK_THRESHOLD = 90  # in percentage
LOG_FILE = "performance_logs.txt"

# Function to log messages
def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(message)

# Performance Monitoring
def monitor_performance(interval=5):
    log_message("Starting Performance Monitoring...")
    
    while True:
        # Monitor CPU
        cpu_usage = psutil.cpu_percent(interval=1)
        if cpu_usage > CPU_THRESHOLD:
            log_message(f"ALERT: High CPU usage detected: {cpu_usage}%")
        
        # Monitor Memory
        memory = psutil.virtual_memory()
        memory_usage = memory.percent
        if memory_usage > MEMORY_THRESHOLD:
            log_message(f"ALERT: High Memory usage detected: {memory_usage}%")
        
        # Monitor Disk
        disk = psutil.disk_usage('/')
        disk_usage = disk.percent
        if disk_usage > DISK_THRESHOLD:
            log_message(f"ALERT: High Disk usage detected: {disk_usage}%")
        
        # Monitor Network
        net = psutil.net_io_counters()
        network_info = f"Sent: {net.bytes_sent / (1024 * 1024):.2f} MB, " \
                       f"Received: {net.bytes_recv / (1024 * 1024):.2f} MB"
        log_message(f"Network Activity - {network_info}")
        
        # Wait for the next interval
        time.sleep(interval)

if __name__ == "__main__":
    try:
        monitor_performance(interval=10)  # Check every 10 seconds
    except KeyboardInterrupt:
        log_message("Performance Monitoring stopped.")
