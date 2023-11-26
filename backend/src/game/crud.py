from sqlalchemy.orm import Session
from src.game import models, util
from src.game.types import Player, GameState
from src.game.pieces import crud


def create_new_game(db: Session):
    db_game = models.Game(
        turn_num=1, player_turn=Player.White, game_state=GameState.Active)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)

    # Now we have to create all the pieces for the game into starting position
    pieces = util.initialize_pieces(db_game.id)
    for piece in pieces:
        db.add(piece)

    db.commit()
    return db_game


def get_all_games(db: Session, skip: int = 0, limit: int = 100, game_state: GameState = GameState.Active):
    return db.query(models.Game).filter(models.Game.game_state == game_state).offset(skip).limit(limit).all()


def get_game(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def update_game_state(db: Session, game_id: int, game_state: GameState):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        return None

    db_game.game_state = game_state
    db.commit()
    db.refresh(db_game)
    return db_game


def delete_game(db: Session, game_id: int):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        return None

    db.delete(db_game)
    db.commit()
    return db_game


def update_turn_number(db: Session, game_id: int):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        return None

    if db_game.player_turn == Player.Black:
        db_game.turn_num += 1

    if db_game.player_turn == Player.White:
        db_game.player_turn = Player.Black
    else:
        db_game.player_turn = Player.White

    db.commit()
    db.refresh(db_game)
    return db_game


def reset_game_state(db: Session, game_id: int):
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if db_game is None:
        return None

    # Reset the game back to the original values
    db_game.game_state = GameState.Active
    db_game.turn_num = 1
    db_game.player_turn = Player.White

    # Delete all game pieces that are to the game ID
    crud.delete_game_pieces_by_game_id(db, game_id)

    # Now reset the game pieces
    pieces = util.initialize_pieces(db_game.id)
    for piece in pieces:
        db.add(piece)

    # Save everything
    db.commit()
    db.refresh(db_game)

    return db_game
