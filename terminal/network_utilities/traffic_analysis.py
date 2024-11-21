import psutil
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from collections import defaultdict
import logging

# Configure logging
logging.basicConfig(
    filename="network_traffic.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
)


# Email alert function
def send_email_alert(subject, body, to_email):
    from_email = "your_email@gmail.com"
    password = "your_email_password"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg["From"] = from_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")


# Function to detect anomalies in traffic data
def detect_anomalies(traffic_data, threshold=5000000):  # Threshold in bytes (5MB)
    total_traffic = sum(traffic_data.values())
    logging.info(f"Total traffic: {total_traffic} bytes")

    # Alert if traffic exceeds threshold
    if total_traffic > threshold:
        send_email_alert(
            "Traffic Spike Detected",
            f"Traffic exceeded threshold: {total_traffic} bytes",
            "admin@example.com",
        )
        logging.warning(f"Traffic spike detected: {total_traffic} bytes")


# Function to capture network usage using psutil
def monitor_network_usage(interface="eth0"):
    net_io = psutil.net_io_counters(pernic=True)
    if interface in net_io:
        bytes_sent = net_io[interface].bytes_sent
        bytes_recv = net_io[interface].bytes_recv
        total_bytes = bytes_sent + bytes_recv
        print(f"Network traffic (bytes): {total_bytes}")
        logging.info(f"Network traffic (bytes): {total_bytes}")
        return total_bytes
    else:
        print(f"Interface {interface} not found.")
        logging.error(f"Interface {interface} not found.")
        return 0


# Function to simulate monitoring traffic
def analyze_traffic(interface="eth0", capture_duration=60):
    traffic_data = defaultdict(int)
    for _ in range(capture_duration):  # Capture data for the duration in seconds
        traffic = monitor_network_usage(interface)
        traffic_data[interface] += traffic
        time.sleep(1)  # Delay to capture traffic over time

    detect_anomalies(traffic_data)

    # Generate a summary report
    report = generate_traffic_report(traffic_data)
    logging.info(f"Traffic analysis report: \n{report}")
    print(report)


# Function to generate a traffic summary report
def generate_traffic_report(traffic_data):
    report = "---- Traffic Analysis Report ----\n"
    report += f"Total Traffic (bytes): {sum(traffic_data.values())}\n"
    for interface, traffic in traffic_data.items():
        report += f"Interface: {interface}, Traffic: {traffic} bytes\n"
    return report


# Main function to continuously monitor and analyze traffic
def main():
    interface = "eth0"  # Set the network interface (e.g., eth0, wlan0)
    while True:
        analyze_traffic(interface, capture_duration=60)  # Analyze traffic for 1 minute
        time.sleep(60)  # Wait before the next round of analysis


if __name__ == "__main__":
    main()
