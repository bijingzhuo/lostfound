import jwt

SECRET = "super-secret-key"  # 可以放入环境变量更安全

def create_token(username: str) -> str:
    # 生成 JWT
    return jwt.encode({"user": username}, SECRET, algorithm="HS256")

def verify_token(token: str) -> str | None:
    # 验证 JWT
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded["user"]
    except jwt.exceptions.InvalidTokenError:
        return None
