from enum import Enum


class Player(Enum):
    White = "White"
    Black = "Black"


class GameState(Enum):
    Completed = "Completed"
    Active = "Active"


class GameResult(Enum):
    White = "White"
    Black = "Black"
    Draw = "Draw"
    Stalemate = "Stalemate"


class PieceType(Enum):
    Pawn = "Pawn"
    King = "King"
    Queen = "Queen"
    Bishop = "Bishop"
    Knight = "Knight"
    Rook = "Rook"


class MoveResult(Enum):
    MoveIsValid = 'MoveIsValid'
