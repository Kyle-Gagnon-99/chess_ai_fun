from typing import Optional

from pydantic import BaseModel
from src.game.types import Player, GameState, GameResult, PieceType


class ChessPiece(BaseModel):
    id: int
    string_id: str
    piece_type: PieceType
    player: Player
    row: int
    col: int
    game_id: int

    class Config:
        from_attributes = True


class ChessPieceMove(ChessPiece):
    from_row: int
    from_col: int
    to_row: int
    to_col: int


class Game(BaseModel):
    id: int
    turn_num: int
    player_turn: Player
    game_state: GameState
    game_result: Optional[GameResult]
    last_en_passant: Optional[str]
    pieces: list[ChessPiece]

    class Config:
        from_attributes = True
