import { ChessPiece, MoveHistory, PieceType, Player } from '@/types/ChessTypes';

export const startGame: ChessPiece[] = [
    // White pieces
    {
        id: 'white-rook-1',
        type: PieceType.Rook,
        player: Player.White,
        position: { row: 7, col: 0 },
    },
    {
        id: 'white-knight-1',
        type: PieceType.Knight,
        player: Player.White,
        position: { row: 7, col: 1 },
    },
    {
        id: 'white-bishop-1',
        type: PieceType.Bishop,
        player: Player.White,
        position: { row: 7, col: 2 },
    },
    {
        id: 'white-queen-1',
        type: PieceType.Queen,
        player: Player.White,
        position: { row: 7, col: 3 },
    },
    {
        id: 'white-king-1',
        type: PieceType.King,
        player: Player.White,
        position: { row: 7, col: 4 },
    },
    {
        id: 'white-bishop-2',
        type: PieceType.Bishop,
        player: Player.White,
        position: { row: 7, col: 5 },
    },
    {
        id: 'white-knight-2',
        type: PieceType.Knight,
        player: Player.White,
        position: { row: 7, col: 6 },
    },
    {
        id: 'white-rook-2',
        type: PieceType.Rook,
        player: Player.White,
        position: { row: 7, col: 7 },
    },
    // White pawns
    ...Array.from({ length: 8 }, (_, col) => ({
        id: `white-pawn-${col}`,
        type: PieceType.Pawn,
        player: Player.White,
        position: { row: 6, col },
    })),
    // Black pieces
    {
        id: 'black-rook-1',
        type: PieceType.Rook,
        player: Player.Black,
        position: { row: 0, col: 0 },
    },
    {
        id: `black-knight-1`,
        type: PieceType.Knight,
        player: Player.Black,
        position: { row: 0, col: 1 },
    },
    {
        id: 'black-bishop-1',
        type: PieceType.Bishop,
        player: Player.Black,
        position: { row: 0, col: 2 },
    },
    {
        id: 'black-queen-1',
        type: PieceType.Queen,
        player: Player.Black,
        position: { row: 0, col: 3 },
    },
    {
        id: 'black-king-1',
        type: PieceType.King,
        player: Player.Black,
        position: { row: 0, col: 4 },
    },
    {
        id: 'black-bishop-2',
        type: PieceType.Bishop,
        player: Player.Black,
        position: { row: 0, col: 5 },
    },
    {
        id: 'black-knight-2',
        type: PieceType.Knight,
        player: Player.Black,
        position: { row: 0, col: 6 },
    },
    {
        id: 'black-rook-2',
        type: PieceType.Rook,
        player: Player.Black,
        position: { row: 0, col: 7 },
    },
    // Black pawns
    ...Array.from({ length: 8 }, (_, col) => ({
        id: `black-pawn-${col}`,
        type: PieceType.Pawn,
        player: Player.Black,
        position: { row: 1, col },
    })),
];

export const fromRowColToLetterNum = (row: number, col: number): string => {
    let number = String(row);
    let letter = '';

    switch (col) {
        case 1:
            letter = 'a';
            break;
        case 2:
            letter = 'b';
            break;
        case 3:
            letter = 'c';
            break;
        case 4:
            letter = 'd';
            break;
        case 5:
            letter = 'e';
            break;
        case 6:
            letter = 'f';
            break;
        case 7:
            letter = 'g';
            break;
        case 8:
            letter = 'h';
            break;
        default:
            letter = 'NA';
            break;
    }

    return `${letter}${number}`;
};

export const fromEnumPieceTypeToLetter = (pieceType: PieceType): string => {
    switch (pieceType) {
        case PieceType.King:
            return 'K';
        case PieceType.Queen:
            return 'Q';
        case PieceType.Bishop:
            return 'B';
        case PieceType.Knight:
            return 'N';
        case PieceType.Rook:
            return 'R';
        case PieceType.Pawn:
            return '';
        default:
            return 'NA';
    }
};

export const historyInfoToLongNotation = (
    piece: ChessPiece,
    fromRow: number,
    fromCol: number,
    toRow: number,
    toCol: number,
    isCapture: boolean,
) => {
    let pieceLetter = fromEnumPieceTypeToLetter(piece.type);
    let fromSpace = fromRowColToLetterNum(fromRow, fromCol);
    let toSpace = fromRowColToLetterNum(toRow, toCol);
    let capture = isCapture ? 'x' : '';
    return `${pieceLetter}${fromSpace}${capture}${toSpace}`;
};

export const historyToLongNotation = (history: MoveHistory) => {
    return historyInfoToLongNotation(
        history.pieceType,
        history.fromPos.row,
        history.fromPos.col,
        history.toPos.row,
        history.toPos.col,
        history.captured != undefined,
    );
};
