import logging
import redis

from fastapi import APIRouter, Depends, HTTPException

from src.dependencies import get_db, get_redis
from src.game import crud, schemas, game_rules
from src.game.pieces import crud as piece_crud
from src.game.types import GameState, MoveResult
from src.redis import store_data, get_data, delete_key

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
async def get_game(game_id: int, db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)):
    game = crud.get_game(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')

    # Before the game is retreived, calculate all of the possible valid moves,
    # then store it in redis
    # This will act as loading the game which will load the memory for further use
    (moves,
     potential_captures) = game_rules.get_all_legal_moves(game)
    game_info = get_data(redis_client=redis_client, key=str(game_id))
    if game_info is None:
        game_info = {}
    game_info['moves'] = moves
    game_info['potential_captures'] = potential_captures
    store_data(redis_client=redis_client, key=str(game_id), data=game_info)

    return game


@router.post('/create', summary='Creates a new chess game. All pieces start in starting position', response_model=schemas.Game)
async def create_new_game(db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)):
    game = crud.create_new_game(db)
    if game is None:
        raise HTTPException(
            status_code=500, detail='An unkown error occurred while trying to create a new game')

    # When a game is created, load the game into the redis cache for ease of use
    (moves,
     potential_captures) = game_rules.get_all_legal_moves(game)
    game_info = get_data(redis_client=redis_client, key=str(game.id))
    if game_info is None:
        game_info = {}
    game_info['moves'] = moves
    game_info['potential_captures'] = potential_captures
    store_data(redis_client=redis_client, key=str(game.id), data=game_info)
    return game


@router.delete('/{game_id}', summary='Deletes a game by id')
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    game = crud.delete_game(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')
    piece_crud.delete_game_pieces_by_game_id(db, game_id)
    return game


@router.post('/{game_id}/reset', summary='Resets the game as if it was just created', response_model=schemas.Game)
async def reset_game(game_id: int, db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)):
    logging.debug(f'Resetting game {game_id}')
    game = crud.get_game(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game id {game_id} was not found')

    # Reset the game state in the database
    game = crud.reset_game_state(db, game_id)

    # Now reload the legal moves cache data in Redis
    delete_key(redis_client, game_id)
    (moves,
     potential_captures) = game_rules.get_all_legal_moves(game)
    game_info = get_data(redis_client=redis_client, key=str(game.id))
    if game_info is None:
        game_info = {}
    game_info['moves'] = moves
    game_info['potential_captures'] = potential_captures
    store_data(redis_client=redis_client, key=str(game.id), data=game_info)

    return game


@router.post('/{game_id}/load_game', summary='Loads the game information into the backend. Typically not needed but can be used')
async def load_game(game_id: int, db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)):
    game = crud.get_game(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')

    # Load the game into memory
    (moves,
     potential_captures) = game_rules.get_all_legal_moves(game)
    game_info = get_data(redis_client=redis_client, key=str(game.id))
    if game_info is None:
        game_info = {}
    game_info['moves'] = moves
    game_info['potential_captures'] = potential_captures
    store_data(redis_client=redis_client, key=str(game.id), data=game_info)


@router.post('/{game_id}/unload_game', summary='Removes any cache data of the current game')
async def unload_game(game_id: int, redis_client: redis.Redis = Depends(get_redis)):
    delete_key(redis_client, str(game_id))
    return f'Unloaded game {game_id}'


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


@router.post('/{game_id}/move', summary='Moves a piece from one position to another', response_model=schemas.MoveResponse)
async def move_game_piece(game_id: int, piece: schemas.ChessPieceMove, db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)):
    game = crud.get_game(db, game_id)
    logging.debug(
        f'Moving piece {piece.string_id} from ({piece.from_col}, {piece.from_row}) to ({piece.to_col}, {piece.to_row}) in game {game_id}')
    is_move_valid, captured_piece = game_rules.validate_move(
        piece, game, redis_client)
    if is_move_valid:
        # Now once the move is valid, we need to update the piece in the database and recalculate the valid moves and then return the game
        # We also need to check if that move was a capture. If so we need to remove the piece from the database and remove it from the cache
        new_move = {
            'row': piece.to_row,
            'col': piece.to_col
        }
        piece = piece_crud.update_piece(db, piece.id, game_id, new_move)
        if piece is None:
            raise HTTPException(
                status_code=400, detail='Unable to update piece. Please make sure ID and Game ID are correct')

        # Now update the moves
        game_info = get_data(redis_client, game_id)
        updated_moves = game_rules.get_list_of_moves(piece, game)
        game_info['moves'][piece.string_id] = updated_moves

        # Now check if a piece was captured
        if captured_piece is not None:
            piece_crud.delete_piece(db, captured_piece, game_id)
            del game_info['moves'][captured_piece]

        store_data(redis_client, game_id, game_info)

    return schemas.MoveResponse(result=MoveResult.MoveIsValid)


@router.get('/{game_id}/legal_moves', summary='Get the list of all legal moves', response_model=schemas.LegalMovesReponse)
async def get_all_legal_moves(game_id: int, db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis)):
    game = crud.get_game(db, game_id)
    if game is None:
        raise HTTPException(
            status_code=404, detail=f'Game with id {game_id} not found')

    # Get the list of moves from redis
    moves_json = get_data(redis_client=redis_client, key=f'{game_id}')
    if moves_json is None:
        raise HTTPException(
            status_code=500, detail=f'Game with id {game_id} was not loaded')
    pydantic_model = schemas.LegalMovesReponse(moves=moves_json['moves'])

    return pydantic_model
