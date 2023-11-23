import logging

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_db
from src.game import crud, schemas, game_rules
from src.game.types import GameState

from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/game',
    tags=['game']
)


@router.get('/games', summary='Gets all games (completed and active)', response_model=list[schemas.Game])
async def get_games_list(game_state: GameState = GameState.Active, skip: int = 0, limit: int = 0, db: Session = Depends(get_db)):
    games = crud.get_all_games(db, game_state=game_state)
    return games


@router.get('/{game_id}', summary='Get the game with the given ID', response_model=schemas.Game)
async def get_game(game_id: int, db: Session = Depends(get_db)):
    game = crud.get_game(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')
    return game


@router.post('/create', summary='Creates a new chess game. All pieces start in starting position', response_model=schemas.Game)
async def create_new_game(db: Session = Depends(get_db)):
    game = crud.create_new_game(db)
    if game is None:
        raise HTTPException(
            status_code=500, detail='An unkown error occurred while trying to create a new game')
    return game


@router.delete('/{game_id}', summary='Deletes a game by id')
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    game = crud.delete_game(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')
    return game


@router.post('/{game_id}/game_state', summary='Updates the state of the game', response_model=schemas.Game)
async def update_game_state(game_id: int, game_state: GameState, db: Session = Depends(get_db)):
    game = crud.update_game_state(db, game_id, game_state)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')
    return game


@router.post('/{game_id}/turn', summary='Updates the turn of the game. It also updates the player\'s turn', response_model=schemas.Game)
async def update_turn_number(game_id: int, db: Session = Depends(get_db)):
    game = crud.update_turn_number(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')
    return game


@router.post('/{game_id}/move', summary='Moves a piece from one position to another', response_model=schemas.Game)
async def move_game_piece(game_id: int, piece: schemas.ChessPieceMove, db: Session = Depends(get_db)):
    logging.debug(
        f'Moving piece {piece.string_id} from ({piece.from_row}, {piece.from_col}) to ({piece.to_row}, {piece.to_col}) in game {game_id}')


@router.get('/{game_id}/legal_moves', summary='Get the list of all legal moves')
async def get_all_legal_moves(game_id: int, db: Session = Depends(get_db)):
    game = crud.get_game(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')
    moves = game_rules.get_all_legal_moves(game)
    print(moves)
    return 'Got something!'
