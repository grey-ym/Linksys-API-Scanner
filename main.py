import requests
import json
import base64

# Your router details
Router_IP = input("Input router IP address: ")
Router_Username = input("Input the username for the router: ") 
Router_Password = input("Input the password for the router: ")

URL_JNAP = f"http://{Router_IP}/JNAP/"

# Step 1: Generating the authentication token using Base64 encoding
authentication_string = f"{Router_Username}:{Router_Password}"
authorization_token = base64.b64encode(authentication_string.encode('utf-8')).decode('utf-8')

print(f"Generated token: {authorization_token}")

# Requesting the list of connected devices
request_action = "http://linksys.com/jnap/devicelist/GetDevices3"

headers = {
    "X-JNAP-Action": request_action,
    "Content-Type": "application/json",
    "X-JNAP-Authorization": f"Basic {authorization_token}"
}

# 0 to get all devices, or use a specific revision number to get changes since that revision
payload = {
    "sinceRevision": 0
}

try:
    print("\nRequesting a list of active devices...")
    response = requests.post(URL_JNAP, headers=headers, data=json.dumps(payload), timeout=10)

    if response.status_code == 200:
        devices_data = response.json()
        print("Successfully retrieved the device list")

        if "output" in devices_data and "devices" in devices_data["output"]:
            print("\nList of active devices: ")
            for device in devices_data["output"]["devices"]:

                # Getting the list of connections for each device
                connections = device.get("connections")

                # Getting only devices with active connections
                device_name = device.get("friendlyName", "Not found")
                if connections or len(connections) > 0: 
                    # Getting the first connection (assuming it's the primary one)
                    ip_address = connections[0].get("ipAddress", "N/A")
                    mac_address = connections[0].get("macAddress", "N/A")
                    print(f" · {ip_address.ljust(14)} | {mac_address.ljust(13)} | {device_name.ljust(25)} ")


    else:
        print(f"Error retrieving device list. Status code: {response.status_code}")
        print(f"Server response: {response.text}")

except requests.exceptions.RequestException as e:
    print(f"Network error: {e}")