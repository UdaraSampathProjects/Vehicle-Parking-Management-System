from flask import Flask, request, jsonify

from prometheus_client import Counter, Gauge, Histogram, generate_latest

import time

from datetime import datetime
 
app = Flask(__name__)
 
# In-memory data storage

vehicles = {}  # {vehicle_id: {"plate": "ABC123", "entry_time": timestamp}}

parking_slots = {

    1: {"occupied": False, "vehicle_id": None},

    2: {"occupied": False, "vehicle_id": None},

    3: {"occupied": False, "vehicle_id": None}

}

logs = []  # List of {vehicle_id, entry_time, exit_time, duration}
 
# Prometheus Metrics

vehicle_entries = Counter("vehicle_entries_total", "Total number of vehicle entries")

vehicle_exits = Counter("vehicle_exits_total", "Total number of vehicle exits")

occupied_slots_gauge = Gauge("occupied_slots", "Number of occupied parking slots")

free_slots_gauge = Gauge("free_slots", "Number of free parking slots")

parking_duration = Histogram("parking_duration_seconds", "Time spent parked")

http_requests_total = Counter("http_requests_total", "Count of HTTP requests", ["method", "endpoint"])

request_latency = Histogram("http_request_duration_seconds", "Request latency", ["method", "endpoint"])
 
# Middleware for HTTP metrics

@app.before_request

def start_timer():

    request.start_time = time.time()
 
@app.after_request

def record_request_data(response):

    if hasattr(request, 'start_time'):

        endpoint = request.url_rule.rule if request.url_rule else "unknown"

        method = request.method

        http_requests_total.labels(method=method, endpoint=endpoint).inc()

        request_latency.labels(method=method, endpoint=endpoint).observe(time.time() - request.start_time)

    return response
 
# Utils

def update_slot_metrics():

    occupied = sum(1 for s in parking_slots.values() if s["occupied"])

    free = len(parking_slots) - occupied

    occupied_slots_gauge.set(occupied)

    free_slots_gauge.set(free)
 
# REST Endpoints

@app.route("/vehicles", methods=["POST"])

def register_vehicle():

    data = request.get_json()

    vehicle_id = str(len(vehicles) + 1)

    vehicles[vehicle_id] = {"plate": data["plate"], "entry_time": None}

    return jsonify({"message": "Vehicle registered", "vehicle_id": vehicle_id}), 201
 
@app.route("/vehicles/<vehicle_id>", methods=["GET"])

def get_vehicle(vehicle_id):

    if vehicle_id not in vehicles:

        return jsonify({"error": "Vehicle not found"}), 404

    return jsonify(vehicles[vehicle_id])
 
@app.route("/vehicles/<vehicle_id>", methods=["PUT"])

def update_vehicle(vehicle_id):

    if vehicle_id not in vehicles:

        return jsonify({"error": "Vehicle not found"}), 404

    data = request.get_json()

    vehicles[vehicle_id]["plate"] = data.get("plate", vehicles[vehicle_id]["plate"])

    return jsonify({"message": "Vehicle updated"})
 
@app.route("/vehicles/<vehicle_id>", methods=["DELETE"])

def delete_vehicle(vehicle_id):

    if vehicle_id not in vehicles:

        return jsonify({"error": "Vehicle not found"}), 404

    # Free any slot this vehicle is occupying

    for slot in parking_slots.values():

        if slot["vehicle_id"] == vehicle_id:

            print(f"Freeing slot during deletion: vehicle {vehicle_id}")

            slot["occupied"] = False

            slot["vehicle_id"] = None

    del vehicles[vehicle_id]

    update_slot_metrics()

    return jsonify({"message": "Vehicle deleted"})
 
@app.route("/slots", methods=["GET"])

def get_slots():

    return jsonify(parking_slots)
 
@app.route("/assign/<vehicle_id>", methods=["POST"])

def assign_slot(vehicle_id):

    if vehicle_id not in vehicles:

        return jsonify({"error": "Vehicle not found"}), 404

    if vehicles[vehicle_id]["entry_time"] is not None:

        return jsonify({"error": "Vehicle already parked"}), 400

    for slot_id, slot in parking_slots.items():

        if not slot["occupied"]:

            slot["occupied"] = True

            slot["vehicle_id"] = vehicle_id

            vehicles[vehicle_id]["entry_time"] = time.time()

            vehicle_entries.inc()

            update_slot_metrics()

            print(f"🚗 Assigned vehicle {vehicle_id} to slot {slot_id}")

            return jsonify({"message": f"Vehicle assigned to slot {slot_id}", "slot_id": slot_id})

    return jsonify({"error": "No free slots available"}), 403
 
@app.route("/release/<int:slot_id>", methods=["POST"])

def release_slot(slot_id):

    if slot_id not in parking_slots:

        return jsonify({"error": "Invalid slot ID"}), 404

    slot = parking_slots[slot_id]

    if not slot["occupied"]:

        return jsonify({"error": "Slot already free"}), 400

    vehicle_id = slot["vehicle_id"]

    entry_time = vehicles[vehicle_id]["entry_time"]

    if entry_time is None:

        return jsonify({"error": "Vehicle was not assigned properly"}), 500

    exit_time = time.time()

    duration = exit_time - entry_time

    slot["occupied"] = False

    slot["vehicle_id"] = None

    vehicles[vehicle_id]["entry_time"] = None

    logs.append({

        "vehicle_id": vehicle_id,

        "entry_time": datetime.fromtimestamp(entry_time).isoformat(),

        "exit_time": datetime.fromtimestamp(exit_time).isoformat(),

        "duration": round(duration, 2)

    })

    vehicle_exits.inc()

    parking_duration.observe(duration)

    update_slot_metrics()

    print(f"🅿️ Released slot {slot_id} from vehicle {vehicle_id}")

    return jsonify({"message": f"Slot {slot_id} released", "duration": duration})
 
@app.route("/logs", methods=["GET"])

def get_logs():

    return jsonify(logs)
 
@app.route("/metrics")

def metrics():

    return generate_latest(), 200, {"Content-Type": "text/plain"}
 
# Optional: Reset everything (for testing)

@app.route("/reset", methods=["POST"])

def reset_system():

    global vehicles, parking_slots, logs

    vehicles = {}

    parking_slots = {

        1: {"occupied": False, "vehicle_id": None},

        2: {"occupied": False, "vehicle_id": None},

        3: {"occupied": False, "vehicle_id": None}

    }

    logs = []

    update_slot_metrics()

    return jsonify({"message": "System reset successful"}), 200

 
if __name__ == "__main__":

    update_slot_metrics()

    app.run(host="0.0.0.0", port=8000)

 