"""
main.py
"""

import uvicorn
from fastapi import FastAPI
from src.routers import product, delivery


app = FastAPI()
app.include_router(product.router)
app.include_router(delivery.router)


@app.get("/")
async def root():
    return {"message": "Web Server Works!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
