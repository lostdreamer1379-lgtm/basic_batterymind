import time
import random
import requests
from datetime import datetime, timedelta
from scipy.io import loadmat


BACKEND_URL = "http://127.0.0.1:5000/battery-data"
SAMPLE_INTERVAL = 1
WINDOW_SIZE = 300


def load_discharge_cycles(mat_path, battery_key):
    mat = loadmat(mat_path)
    cycles = mat[battery_key][0, 0]['cycle'][0]
    return [c for c in cycles if c['type'][0] == 'discharge']


def cycle_to_readings(cycle):
    data = cycle['data'][0, 0]
    V = data['Voltage_measured'].flatten()
    I = data['Current_measured'].flatten()
    T = data['Temperature_measured'].flatten()
    t = data['Time'].flatten()
    return V, I, T, t


print("=" * 60)
print("BatteryMind Sensor Simulator (Real Cycle Replay)")
print("=" * 60)

MAT_PATH = "../4. BatteryAgingARC_45_46_47_48/B0045.mat"
discharge_cycles = load_discharge_cycles(MAT_PATH, "B0045")

print(f"\nLoaded {len(discharge_cycles)} discharge cycles.\n")
print("Select Test Battery")
print("1. New (early cycle)")
print("2. Mid-life (~50% through)")
print("3. Aged (late cycle)\n")

choice = input("Choice : ")
bucket = {
    "1": discharge_cycles[0],
    "2": discharge_cycles[len(discharge_cycles) // 2],
    "3": discharge_cycles[-1],
}
cycle = bucket.get(choice, discharge_cycles[0])

V, I, T, t = cycle_to_readings(cycle)
print(f"Replaying real cycle with {len(V)} samples over {t[-1]-t[0]:.0f}s\n")

# Reset the backend's feature buffer and size it EXACTLY to this
# cycle's sample count, so nothing from a previous run leaks in
# and nothing from this cycle gets truncated off the front.
try:
    reset_response = requests.post(
        "http://127.0.0.1:5000/reset",
        json={"window_size": len(V)},
        timeout=5
    )
    reset_data = reset_response.json()
    print("Reset backend:", reset_data)

    if reset_data.get("window_size") != len(V):
        print(f"WARNING: window_size mismatch! Expected {len(V)}, "
              f"backend reports {reset_data.get('window_size')}")
except Exception as e:
    print("Reset failed:", e)

virtual_start_time = datetime.now()

for i in range(len(V)):
    payload = {
        "voltage": round(float(V[i]), 3),
        "current": round(float(abs(I[i])), 3),
        "temperature": round(float(T[i]), 2),
        "timestamp": (virtual_start_time + timedelta(seconds=float(t[i] - t[0]))).isoformat(),
    }

    try:
        response = requests.post(BACKEND_URL, json=payload, timeout=5)
        result = response.json()

        print(f"Sample {i+1}/{len(V)}", payload)

        if result.get("status") == "success":
            prediction = result["prediction"]
            print("MODEL OUTPUT")
            print("SOH:", prediction["soh"])
            print("Health:", prediction["health"])
            print("Risk:", prediction["risk"])

    except Exception as e:
        print("Backend error:", e)

    time.sleep(SAMPLE_INTERVAL)

print("\nCycle completed")