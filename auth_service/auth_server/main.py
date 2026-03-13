from fastapi import FastAPI
from auth_server.routers import routers
import uvicorn

app = FastAPI(
    title="Auth Service"
)

app.include_router(routers)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )