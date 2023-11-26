from sqlalchemy.orm import Session

from src.game import models
from src.game.types import Player


def get_all_pieces(db: Session, game_id: int, player: Player | None):
    if player is None:
        return db.query(models.Piece).filter(models.Piece.game_id == game_id).all()
    else:
        return db.query(models.Piece).filter(models.Piece.game_id == game_id).filter(models.Piece.player == str(player.value)).all()


def update_piece(db: Session, piece_id: int, game_id: int, new_data: dict):
    # Query for a specific piece
    piece = db.query(models.Piece).filter(models.Piece.game_id ==
                                          game_id).filter(models.Piece.id == piece_id).first()

    # If the piece was not found in the database, return None
    if piece is None:
        return None

    # Update the piece's attributes
    for key, value in new_data.items():
        setattr(piece, key, value)

    # Commit the changes
    db.commit()

    # Return the piece
    return piece


def delete_piece(db: Session, piece_string_id: str, game_id: int):
    piece = db.query(models.Piece).filter(models.Piece.id ==
                                          game_id).filter(models.Piece.string_id == piece_string_id).first()

    if piece is None:
        return None

    db.delete(piece)
    db.commit()
    return piece


def delete_game_pieces_by_game_id(db: Session, game_id: int):
    pieces = db.query(models.Piece).filter(
        models.Piece.game_id == game_id).all()

    for p in pieces:
        db.delete(p)

    db.commit()
