import logging

from app.routers import hello
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    """Creates the fastapi application

    Returns:
        FastAPI: the fastapi app
    """
    origins = [
        "http://localhost:4200",
    ]
    application = FastAPI()

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(hello.router)
    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    """executes on application startup"""
    log.info("----Starting up----")


@app.on_event("shutdown")
async def shutdown_event():
    """executes on application shutdown"""
    log.info("----Shutting down----")
