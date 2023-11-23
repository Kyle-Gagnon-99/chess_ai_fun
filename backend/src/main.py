from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.game.api import router as chess_router
from src.config import cors_origins
from src.database import engine
from . import database
from src.logging import configure_logging

database.Base.metadata.create_all(bind=engine)

app = FastAPI()
configure_logging()
app.include_router(chess_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
