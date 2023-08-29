# monitor/main.py

from fastapi import FastAPI
from api.routers import router as api_router

app = FastAPI()

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000,) # host="0.0.0.0"
