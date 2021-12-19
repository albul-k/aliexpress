import os
from fastapi import Header, HTTPException
from dotenv import load_dotenv


load_dotenv('.env')
X_TOKEN = os.environ.get('X_TOKEN')


async def get_token_header(x_token: str = Header(...)):
    if x_token != X_TOKEN:
        raise HTTPException(status_code=401, detail="X-Token header is invalid")
