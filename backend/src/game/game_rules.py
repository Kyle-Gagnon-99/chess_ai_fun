import redis

from src.game import schemas
from src.game.types import PieceType, Player
from src.redis import get_data

MAX_ROW_NUM = 8
MAX_COL_NUM = 8


class InvalidMoveException(Exception):
    def __init__(self, message: str):
        self.message = message


def validate_move(piece: schemas.ChessPieceMove, game: schemas.Game, redis_client: redis.Redis):
    # Get the list of all pieces belonging to the game
    pieces = game.pieces

    # We need to validate first that the piece exists in the game
    piece_exists = False
    for p in pieces:
        if p.id == piece.id and p.string_id == piece.string_id:
            piece_exists = True
            break

    # If the piece doesn't exist, we can't move it
    if not piece_exists:
        raise InvalidMoveException(
            f'Piece with id {piece.id} does not exist in game {game.id}')

    # If the piece does exist, first we need to check to make sure that the piece being moved belongs to the current player
    if piece.player != game.player_turn:
        raise InvalidMoveException(
            f'Piece with id {piece.id} does not belong to the current player')

    # Check if the target position is a move that the given piece can make
    game_info = get_data(redis_client, str(game.id))
    if not game_info or 'moves' not in game_info:
        raise InvalidMoveException("Game moves data not found", piece)

    # Convert list of lists to list of tuples
    piece_moves = [tuple(move)
                   for move in game_info['moves'].get(piece.string_id, [])]

    # Check if the target move was in the liast
    target_move = (piece.to_col, piece.to_row)
    if target_move not in piece_moves:
        raise InvalidMoveException(
            message=f'Move {target_move} is not valid for {piece.string_id}')

    # Also check if the move was a capture. If so return the piece that was captured
    captured_piece = None
    for key, value in game_info['moves'].items():
        piece_moves = [tuple(move) for move in value]
        if target_move in piece_moves:
            captured_piece = key

    return True, captured_piece


def get_all_legal_moves(game: schemas.Game):
    legal_moves = {}
    potential_captures_dict = {}
    for p in game.pieces:
        (moves, potential_captures) = get_list_of_moves(p, game)
        legal_moves[p.string_id] = moves

        if not p.player.value in potential_captures_dict:
            potential_captures_dict[p.player.value] = {}

        potential_captures_dict[p.player.value][p.string_id] = potential_captures
    return (legal_moves, potential_captures_dict)


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
    elif piece_type == PieceType.Queen:
        return get_queen_move_list(piece, game)
    elif piece_type == PieceType.King:
        return get_king_move_list(piece, game)
    else:
        return ([], [])


def get_pawn_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    potential_captures = []
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

    # Handle en passant
    if game.last_en_passant is not None:
        en_passant_piece = None
        for p in game.pieces:
            if p.string_id == game.last_en_passant:
                en_passant_piece = p

        if en_passant_piece is not None:
            # Now check to see if the current pawn is in the right row to do an en passant
            if piece.row == (3 if piece.player == Player.Black else 6):
                # Then check if the current pawn piece was next to the en passant piece
                if piece.col == en_passant_piece.col - 1 or piece.col == en_passant_piece.col + 1:
                    moves.append((piece.row + (1 * row_direction), piece.col))

    # Captures
    for capture_col in [piece.col - 1, piece.col + 1]:
        exists, cap_piece = piece_exists_in_target(
            row=forward_row, col=capture_col, game=game, enemy=Player.White if piece.player == Player.Black else Player.Black)
        if exists:
            moves.append((capture_col, forward_row))
            potential_captures.append(cap_piece.string_id)

    return moves, potential_captures


def get_knight_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    potential_captures = []
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
                exists, cap_piece = piece_exists_in_target(
                    col=move[0], row=move[1], game=game, enemy=Player.White if piece.player == Player.Black else Player.Black)
                if exists:
                    moves.append(move)
                    potential_captures.append(cap_piece.string_id)

    return moves, potential_captures


def get_king_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    potential_captures = []
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
                exists, cap_piece = piece_exists_in_target(
                    col=move[0], row=move[1], game=game, enemy=Player.White if piece.player == Player.Black else Player.Black)
                if exists:
                    moves.append(move)
                    potential_captures.append(cap_piece.string_id)

    return moves, potential_captures


def get_rook_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    potential_captures = []

    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=0, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=0, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=0, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=0, delta_row=-1, game=game, player=piece.player)

    return moves, potential_captures


def get_bishop_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    potential_captures = []

    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=-1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=-1, game=game, player=piece.player)

    return moves, potential_captures


def get_queen_move_list(piece: schemas.ChessPieceMove, game: schemas.Game):
    moves = []
    potential_captures = []

    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=0, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=0, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=0, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=0, delta_row=-1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=1, delta_row=-1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=1, game=game, player=piece.player)
    add_moves_in_direction(moves=moves, potential_captures=potential_captures, start_col=piece.col, start_row=piece.row,
                           delta_col=-1, delta_row=-1, game=game, player=piece.player)

    return moves, potential_captures


def add_moves_in_direction(moves: list[(int, int)], potential_captures: list[schemas.ChessPiece], start_col: int, start_row: int, delta_col: int, delta_row: int, game: schemas.Game, player: Player):
    col, row = start_col, start_row
    while True:
        col += delta_col
        row += delta_row
        if not (1 <= row <= MAX_ROW_NUM and 1 <= col <= MAX_COL_NUM):
            break
        if any_piece_exists_in_target(col=col, row=row, game=game):
            exists, piece = piece_exists_in_target(
                col=col, row=row, game=game, enemy=Player.White if player == Player.Black else Player.Black)
            if exists:
                moves.append((col, row))
                potential_captures.append(piece.string_id)
            break
        else:
            moves.append((col, row))


def piece_exists_in_target(col: int, row: int, game: schemas.Game, enemy: Player):
    # Check if the space is in bounds
    if not (1 <= row <= 8 and 1 <= col <= 8):
        return False, None

    for p in game.pieces:
        if p.player == enemy and p.row == row and p.col == col:
            return True, schemas.ChessPiece.model_validate(p)
    return False, None


def any_piece_exists_in_target(col: int, row: int, game: schemas.Game):
    # Check if the space is in bounds
    if not (1 <= row <= 8 and 1 <= col <= 8):
        return False

    for p in game.pieces:
        if p.row == row and p.col == col:
            return True
    return False
