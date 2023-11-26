from fastapi import APIRouter, HTTPException, Depends

from src.dependencies import get_db
from src.game import schemas as game_schemas
from src.game.types import Player
from src.game.pieces import crud

from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/game',
    tags=['pieces']
)


@router.get('/{game_id}/pieces', summary='Gets all of the pieces of the game', response_model=list[game_schemas.ChessPiece])
async def get_pieces(game_id: int, db: Session = Depends(get_db), player: Player | None = None):
    pieces = crud.get_all_pieces(db, game_id, player)
    if pieces is None:
        raise HTTPException(
            status_code=404, detail=f'Unable to find peices for game {game_id}')
    return pieces
