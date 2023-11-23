import logging

from src.game import schemas
from src.game.types import PieceType, Player

MAX_ROW_NUM = 8
MAX_COL_NUM = 8


class InvalidMoveException(Exception):
    def __init__(self, message, move: schemas.ChessPieceMove):
        self.message = message
        self.move = move


def validate_move(piece: schemas.ChessPieceMove, game: schemas.Game):
    # Get the list of all pieces belonging to the game
    pieces = game.pieces

    # We need to validate first that the piece exists in the game
    piece_exists = False
    for p in pieces:
        if p.id == piece.id:
            piece_exists = True
            break

    # If the piece doesn't exist, we can't move it
    if not piece_exists:
        raise InvalidMoveException(
            f'Piece with id {piece.id} does not exist in game {game.id}', piece)

    # If the piece does exist, first we need to check to make sure that the piece being moved belongs to the current player
    if piece.player != game.player_turn:
        raise InvalidMoveException(
            f'Piece with id {piece.id} does not belong to the current player', piece)


def get_all_legal_moves(game: schemas.Game):
    legal_moves = {}
    for p in game.pieces:
        moves = get_list_of_moves(p, game)
        legal_moves[p.string_id] = moves
    return legal_moves


def get_list_of_moves(piece: schemas.ChessPieceMove, game: schemas.Game):
    piece_type = piece.piece_type

    if piece_type == PieceType.Pawn:
        return get_pawn_move_list(piece, game)
    elif piece_type == PieceType.Rook:
        return get_rook_move_list(piece, game)
    elif piece_type == PieceType.Bishop:
        return get_bishop_move_list(piece, game)
    elif piece_type == PieceType.Knight:
        return get_knight_move_list(piece, game)
    elif piece_type == PieceType.King:
        return get_king_move_list(piece, game)
    else:
        return []


def get_pawn_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    row_direction = 1 if piece.player == Player.White else -1
    forward_row = piece.row + row_direction

    # Forward moves
    if not any_piece_exists_in_target(row=forward_row, col=piece.col, game=game):
        moves.append((piece.col, forward_row))

        # Starting position
        if piece.row == (2 if piece.player == Player.White else 7):
            double_forward_row = piece.row + 2 * row_direction
            if not any_piece_exists_in_target(row=double_forward_row, col=piece.col, game=game):
                moves.append((piece.col, double_forward_row))

    # Captures
    for capture_col in [piece.col - 1, piece.col + 1]:
        if piece_exists_in_target(row=forward_row, col=capture_col, game=game, enemy=Player.White if piece.player == Player.Black else Player.Black):
            moves.append((capture_col, forward_row))

    return moves


def get_knight_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    potential_moves = [
        (piece.col + 2, piece.row + 1),
        (piece.col + 2, piece.row - 1),
        (piece.col - 2, piece.row + 1),
        (piece.col - 2, piece.row - 1),
        (piece.col + 1, piece.row + 2),
        (piece.col + 1, piece.row - 2),
        (piece.col - 1, piece.row + 2),
        (piece.col - 1, piece.row - 2),
    ]

    for move in potential_moves:
        if (1 <= move[0] <= MAX_ROW_NUM and 1 <= move[1] <= MAX_COL_NUM):
            if not any_piece_exists_in_target(col=move[0], row=move[1], game=game):
                moves.append(move)
            else:
                if piece_exists_in_target(col=move[0], row=move[1], game=game, enemy=Player.White if piece.player == Player.Black else Player.Black):
                    moves.append(move)

    return moves


def get_king_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    potential_moves = [
        (piece.col + 1, piece.row),
        (piece.col - 1, piece.row),
        (piece.col, piece.row + 1),
        (piece.col, piece.row - 1),
        (piece.col + 1, piece.row + 1),
        (piece.col + 1, piece.row - 1),
        (piece.col - 1, piece.row + 1),
        (piece.col - 1, piece.row - 1),
    ]

    for move in potential_moves:
        if (1 <= move[0] <= MAX_ROW_NUM and 1 <= move[1] <= MAX_COL_NUM):
            if not any_piece_exists_in_target(col=move[0], row=move[1], game=game):
                moves.append(move)
            else:
                if piece_exists_in_target(col=move[0], row=move[1], game=game, enemy=Player.White if piece.player == Player.Black else Player.Black):
                    moves.append(move)

    return moves


def get_rook_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []

    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=0, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=0, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=0, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=0, delta_row=-1, game=game, player=piece.player)

    return moves


def get_bishop_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []

    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=-1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=-1, game=game, player=piece.player)

    return moves


def get_queen_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []

    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=0, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=0, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=0, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=0, delta_row=-1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=-1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=-1, game=game, player=piece.player)

    return moves


def add_moves_in_direction(moves: list[(int, int)], start_col: int, start_row: int, delta_col: int, delta_row: int, game: schemas.Game, player: Player):
    col, row = start_col, start_row
    while True:
        col += delta_col
        row += delta_row
        if not (1 <= row <= MAX_ROW_NUM and 1 <= col <= MAX_COL_NUM):
            break
        if any_piece_exists_in_target(col=col, row=row, game=game):
            if piece_exists_in_target(col=col, row=row, game=game, enemy=Player.White if player == Player.Black else Player.Black):
                moves.append((col, row))
            break
        else:
            moves.append((col, row))


def piece_exists_in_target(col: int, row: int, game: schemas.Game, enemy: Player):
    # Check if the space is in bounds
    if not (1 <= row <= 8 and 1 <= col <= 8):
        return False

    for p in game.pieces:
        if p.player == enemy and p.row == row and p.col == col:
            return True
    return False


def any_piece_exists_in_target(col: int, row: int, game: schemas.Game):
    # Check if the space is in bounds
    if not (1 <= row <= 8 and 1 <= col <= 8):
        return False

    for p in game.pieces:
        if p.row == row and p.col == col:
            return True
    return False
