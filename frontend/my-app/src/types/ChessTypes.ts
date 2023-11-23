export enum PieceType {
    King,
    Queen,
    Bishop,
    Knight,
    Rook,
    Pawn,
}

export enum Player {
    White,
    Black,
}

export interface ChessPiece {
    id: string;
    type: PieceType;
    player: Player;
    position: {
        row: number;
        col: number;
    };
}

export interface MoveHistory {
    id: string;
    turnNum: number;
    currentPlayerTurn: Player;
    pieceType: ChessPiece;
    fromPos: {
        row: number;
        col: number;
    };
    toPos: {
        row: number;
        col: number;
    };
    captured?: ChessPiece;
}
