from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import HTTPException, Depends
import os

axidex_username = "axidex"
axidex_password = str(os.environ["PASSWORD_AUTH"])
# FastAPI Security 
##################
security = HTTPBasic()
users_db = {
    axidex_username: {
        "password": axidex_password,
    }
}
def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user = users_db.get(credentials.username)
    if user is None or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return user