import requests
 
import time
 
import random
 
BASE_URL = "http://localhost:8000"
 
def register_vehicle(plate):
 
    res = requests.post(f"{BASE_URL}/vehicles", json={"plate": plate})
 
    return res.json().get("vehicle_id")
 
def assign_vehicle(vehicle_id):
 
    return requests.post(f"{BASE_URL}/assign/{vehicle_id}")
 
def release_vehicle(slot_id):
 
    return requests.post(f"{BASE_URL}/release/{slot_id}")
 
def get_vehicle(vehicle_id):
 
    return requests.get(f"{BASE_URL}/vehicles/{vehicle_id}")
 
def update_vehicle(vehicle_id):
 
    new_plate = f"XYZ{random.randint(100,999)}"
 
    return requests.put(f"{BASE_URL}/vehicles/{vehicle_id}", json={"plate": new_plate})
 
def delete_vehicle(vehicle_id):
 
    return requests.delete(f"{BASE_URL}/vehicles/{vehicle_id}")
 
def get_slots():
 
    return requests.get(f"{BASE_URL}/slots")
 
def simulate():
 
    plate = f"ABC{random.randint(100,999)}"
 
    print(f"\nRegistering vehicle: {plate}")
 
    vehicle_id = register_vehicle(plate)
 
    if not vehicle_id:
 
        print("Failed to register vehicle.")
 
        return
 
    # GET vehicle info
 
    print(f"Getting vehicle {vehicle_id}")
 
    print(get_vehicle(vehicle_id).json())
 
    # Update vehicle
 
    print(f"Updating vehicle {vehicle_id}")
 
    print(update_vehicle(vehicle_id).json())
 
    # GET slots
 
    print("Checking slot availability...")
 
    print(get_slots().json())
 
    # Assign to slot
 
    print(f"Assigning vehicle {vehicle_id}")
 
    assign_response = assign_vehicle(vehicle_id)
 
    print(assign_response.json())
 
    # Simulate parking time
 
    time.sleep(random.randint(5, 10))
 
    # Release slot
 
    slot_id = random.randint(1, 3)
 
    print(f"Releasing slot {slot_id}")
 
    print(release_vehicle(slot_id).json())
 
    # Delete vehicle
 
    print(f"Deleting vehicle {vehicle_id}")
 
    print(delete_vehicle(vehicle_id).json())
 
# Run this in a loop
 
while True:
 
    try:
 
        simulate()
 
        time.sleep(5)
 
    except KeyboardInterrupt:
 
        print("Stopped simulation.")
 
        break
 