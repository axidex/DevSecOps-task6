import time
from functools import wraps
from fastapi import HTTPException, status
# Limiter
#########
# https://youtu.be/49oC1uHxJ-o?si=YbChXV5XsxJA75eQ
def rateLimited(maxCalls: int, timeFrame: int):
    def decorator(func):
        calls = []

        @wraps(func)
        async def wrapper(*args, **kwargs):
            now = time.time()
            callsInTimeFrame = [call for call in calls if call > now - timeFrame]

            if len(callsInTimeFrame) >= maxCalls:
                raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail="Rate limit exceeded")
            
            calls.append(now)
            return await func(*args, **kwargs)
        return wrapper
    return decorator