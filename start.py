import subprocess
import time
import os

# Files paths for each microservice
services = {
    "Orders": "orders/orders_service.py",
    "Kitchen": "kitchen/kitchen_service.py",
    "Payments": "payments/payments_service.py",
    "Gateway": "api_gateway/gateway.py"
}

processes = []

# Open each service in a new command prompt window
for name, path in services.items():
    full_path = os.path.abspath(path)
    proc = subprocess.Popen(f'start cmd /k python "{full_path}"', shell=True)
    processes.append(proc)
    time.sleep(1)  # Wait a bit to ensure the window opens before starting the next one

