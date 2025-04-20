import requests

USER_SERVICE_URL = "http://localhost:8001/validate"

def verify_token(token: str) -> str | None:
    try:
        res = requests.get(USER_SERVICE_URL, params={"token": token})
        if res.status_code == 200:
            return res.json()["username"]
        else:
            return None
    except:
        return None
