import requests

resp = requests.post(
    "http://127.0.0.1:5000/reset",
    json={"window_size": 490},
    timeout=5
)
print("Status code:", resp.status_code)
print("Raw response:")
print(resp.text)