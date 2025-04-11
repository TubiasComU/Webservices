import subprocess
import psutil
import time
import os

# Function to stop a service by its script name
def stop_service(script_name):
    # Iterate through all running processes
    for proc in psutil.process_iter(attrs=['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info['cmdline']
            if cmdline and any(script_name in part for part in cmdline):
                print(f"Stopping {script_name} with PID {proc.info['pid']}")
                proc.terminate()  # Try to terminate the process
                proc.wait(timeout=1)  # Wait for the process to terminate
        except psutil.TimeoutExpired:
            print(f"Force killing {script_name} with PID {proc.info['pid']}")
            proc.kill()  # Force kill if it doesn't terminate in time
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

# Microservices scripts to stop
services = [
    "orders_service.py",
    "kitchen_service.py",
    "payments_service.py",
    "gateway.py"
]

# For each service, stop the process if it's running
for service in services:
    stop_service(service)

print("All services stopped.")
