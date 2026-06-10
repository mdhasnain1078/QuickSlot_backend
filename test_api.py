import requests

try:
    res = requests.get("http://127.0.0.1:8000/api/v1/users/user1_id/bookings")
    print(res.status_code)
    print(res.json())
except Exception as e:
    print(e)
