import socket


def get_network_ip():
    try:
        # Connect to a public server and immediately close the connection
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            # Use Google's public DNS server to find the network IP
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
    except Exception as e:
        ip = None
    return ip
