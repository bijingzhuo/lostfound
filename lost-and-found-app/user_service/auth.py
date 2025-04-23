import jwt

SECRET = "super-secret-key" 

def create_token(username: str) -> str:
    return jwt.encode({"user": username}, SECRET, algorithm="HS256")

def verify_token(token: str) -> str | None:
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded["user"]
    except jwt.exceptions.InvalidTokenError:
        return None
