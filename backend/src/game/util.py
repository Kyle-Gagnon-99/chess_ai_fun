from src.game.models import Piece

from src.game.types import Player, PieceType


def initialize_pieces(game_id: int) -> list[Piece]:
    pieces = []

    # Add white pieces
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Rook,
                  player=Player.White, string_id='white-rook-1', row=1, col=1))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Knight,
                  player=Player.White, string_id='white-knight-1', row=1, col=2))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Bishop,
                  player=Player.White, string_id='white-bishop-1', row=1, col=3))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Queen,
                  player=Player.White, string_id='white-queen', row=1, col=4))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.King,
                  player=Player.White, string_id='white-king', row=1, col=5))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Bishop,
                  player=Player.White, string_id='white-bishop-2', row=1, col=6))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Knight,
                  player=Player.White, string_id='white-knight-2', row=1, col=7))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Rook,
                  player=Player.White, string_id='white-rook-2', row=1, col=8))

    # Add black pieces
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Rook,
                  player=Player.Black, string_id='black-rook-1', row=8, col=1))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Knight,
                  player=Player.Black, string_id='black-knight-1', row=8, col=2))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Bishop,
                  player=Player.Black, string_id='black-bishop-1', row=8, col=3))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Queen,
                  player=Player.Black, string_id='black-queen', row=8, col=4))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.King,
                  player=Player.Black, string_id='black-king', row=8, col=5))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Bishop,
                  player=Player.Black, string_id='black-bishop-2', row=8, col=6))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Knight,
                  player=Player.Black, string_id='black-knight-2', row=8, col=7))
    pieces.append(Piece(game_id=game_id, piece_type=PieceType.Rook,
                  player=Player.Black, string_id='black-rook-2', row=8, col=8))

    # Add all pawns
    for i in range(8):
        pieces.append(Piece(game_id=game_id, piece_type=PieceType.Pawn,
                      player=Player.White, string_id=f'white-pawn-{i}', row=2, col=i + 1))
        pieces.append(Piece(game_id=game_id, piece_type=PieceType.Pawn,
                      player=Player.Black, string_id=f'black-pawn-{i}', row=7, col=i + 1))

    return pieces
