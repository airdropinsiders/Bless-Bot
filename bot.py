import requests
from colorama import Fore
import json
import time
from datetime import datetime, timezone

API_BASE_URL = "https://gateway-run.bls.dev/api/v1"
IP_SERVICE_URL = "https://tight-block-2413.txlabs.workers.dev"

# Fungsi membaca file 'id.txt'
def read_node_and_hardware_id():
    with open("id.txt", "r") as file:
        data = file.read().strip()
        node_id, hardware_id = data.split(":")
        return node_id, hardware_id

# Fungsi membaca file 'user.txt'
def read_auth_token():
    with open("user.txt", "r") as file:
        return file.read().strip()

# Fungsi mendapatkan IP address dari layanan eksternal
def fetch_ip_address():
    response = requests.get(IP_SERVICE_URL)
    response.raise_for_status()
    data = response.json()
    print(f"[{datetime.now(timezone.utc).isoformat()}] IP fetch response:", data)
    return data["ip"]

# Fungsi mendaftarkan node
def register_node(node_id, hardware_id):
    auth_token = read_auth_token()
    register_url = f"{API_BASE_URL}/nodes/{node_id}"
    ip_address = fetch_ip_address()
    print(f"[{datetime.now(timezone.utc).isoformat()}] Registering node with IP: {ip_address}, Hardware ID: {hardware_id}")
    
    payload = {"ipAddress": ip_address, "hardwareId": hardware_id}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {auth_token}"
    }
    
    response = requests.post(register_url, headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    print(f"[{datetime.now(timezone.utc).isoformat()}] Registration response:", data)
    return data

# Fungsi memulai sesi
def start_session(node_id):
    auth_token = read_auth_token()
    start_session_url = f"{API_BASE_URL}/nodes/{node_id}/start-session"
    print(f"[{datetime.now(timezone.utc).isoformat()}] Starting session for node {node_id}, it might take a while...")
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(start_session_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(f"[{datetime.now(timezone.utc).isoformat()}] Start session response:", data)
    return data

# Fungsi menghentikan sesi
def stop_session(node_id):
    auth_token = read_auth_token()
    stop_session_url = f"{API_BASE_URL}/nodes/{node_id}/stop-session"
    print(f"[{datetime.now(timezone.utc).isoformat()}] Stopping session for node {node_id}")
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(stop_session_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    print(f"[{datetime.now(timezone.utc).isoformat()}] Stop session response:", data)
    return data

# Fungsi untuk ping node
def ping_node(node_id):
    auth_token = read_auth_token()
    ping_url = f"{API_BASE_URL}/nodes/{node_id}/ping"
    print(f"[{datetime.now(timezone.utc).isoformat()}] Pinging node {node_id}")
    
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(ping_url, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    last_ping = data["pings"][-1]["timestamp"]
    log_message = (f"[{datetime.now(timezone.utc).isoformat()}] Ping response, "
                   f"ID: {data['_id']}, NodeID: {data['nodeId']}, Last Ping: {last_ping}")
    print(log_message)
    return data

# Header tampilan
def display_header():
    custom_ascii_art = f"""
    {Fore.CYAN}
         █████╗ ██╗██████╗ ██████╗ ██████╗  ██████╗ ██████╗ 
        ██╔══██╗██║██╔══██╗██╔══██╗██╔══██╗██╔═══██╗██╔══██╗
        ███████║██║██████╔╝██║  ██║██████╔╝██║   ██║██████╔╝
        ██╔══██║██║██╔══██╗██║  ██║██╔══██╗██║   ██║██╔═══╝ 
        ██║  ██║██║██║  ██║██████╔╝██║  ██║╚██████╔╝██║     
        ╚═╝  ╚═╝╚═╝╚═╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝     

        ██╗███╗   ██╗███████╗██╗██████╗ ███████╗██████╗     
        ██║████╗  ██║██╔════╝██║██╔══██╗██╔════╝██╔══██╗    
        ██║██╔██╗ ██║███████╗██║██║  ██║█████╗  ██████╔╝    
        ██║██║╚██╗██║╚════██║██║██║  ██║██╔══╝  ██╔══██╗    
        ██║██║ ╚████║███████║██║██████╔╝███████╗██║  ██║    
        ╚═╝╚═╝  ╚═══╝╚══════╝╚═╝╚═════╝ ╚══════╝╚═╝  ╚═╝{Fore.RESET}
    """
    
    print(custom_ascii_art)
    print(f"{Fore.YELLOW}BLESS NETWORK BOT")
    print("Telegram : t.me/AirdropInsiderID", Fore.RESET)
    print(f"\n")
    

# Fungsi utama
def run_all():
    try:
        display_header()
        node_id, hardware_id = read_node_and_hardware_id()
        print(f"[{datetime.now(timezone.utc).isoformat()}] Read nodeId: {node_id}, hardwareId: {hardware_id}")
        
        registration_response = register_node(node_id, hardware_id)
        print(f"[{datetime.now(timezone.utc).isoformat()}] Node registration completed. Response:", registration_response)
        
        start_session_response = start_session(node_id)
        print(f"[{datetime.now(timezone.utc).isoformat()}] Session started. Response:", start_session_response)
        
        print(f"[{datetime.now(timezone.utc).isoformat()}] Sending initial ping...")
        ping_node(node_id)
        
        while True:
            print(f"[{datetime.now(timezone.utc).isoformat()}] Sending ping...")
            ping_node(node_id)
            time.sleep(60)
    
    except Exception as error:
        print(f"[{datetime.now(timezone.utc).isoformat()}] An error occurred:", error)

if __name__ == "__main__":
    run_all()
