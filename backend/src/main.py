from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.game.api import router as chess_router
from src.game.pieces.api import router as pieces_router
from src.game.game_rules import InvalidMoveException
from src.config import cors_origins
from src.database import engine
from . import database
from src.logging import configure_logging

database.Base.metadata.create_all(bind=engine)

app = FastAPI()
configure_logging()
app.include_router(chess_router)
app.include_router(pieces_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.exception_handler(InvalidMoveException)
async def invalid_move_exception_handler(request: Request, exc: InvalidMoveException):
    return JSONResponse(
        status_code=400,
        content={'message': f"InvalidMove: {exc.message}"}
    )

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
