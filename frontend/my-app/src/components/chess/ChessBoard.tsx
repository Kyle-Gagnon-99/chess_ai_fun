'use client';
import React, { useState } from 'react';
import ChessSquare from './ChessSquare';
import { ChessPiece, MoveHistory, PieceType, Player } from '@/types/ChessTypes';
import KingLight from './pieces/KingLight';
import KingDark from './pieces/KingDark';
import QueenLight from './pieces/QueenLight';
import QueenDark from './pieces/QueenDark';
import BishopLight from './pieces/BishopLight';
import BishopDark from './pieces/BishopDark';
import KnightLight from './pieces/KnightLight';
import KnightDark from './pieces/KnightDark';
import RookLight from './pieces/RookLight';
import RookDark from './pieces/RookDark';
import PawnLight from './pieces/PawnLight';
import PawnDark from './pieces/PawnDark';
import { historyToLongNotation, startGame } from '@/lib/chessUtils';
import { Button } from '../ui/button';

const renderPiece = (piece?: ChessPiece) => {
    if (piece) {
        switch (piece.type) {
            case PieceType.King:
                return piece.player === Player.White ? (
                    <KingLight />
                ) : (
                    <KingDark />
                );
            case PieceType.Queen:
                return piece.player === Player.White ? (
                    <QueenLight />
                ) : (
                    <QueenDark />
                );
            case PieceType.Bishop:
                return piece.player === Player.White ? (
                    <BishopLight />
                ) : (
                    <BishopDark piece={piece} />
                );
            case PieceType.Knight:
                return piece.player === Player.White ? (
                    <KnightLight />
                ) : (
                    <KnightDark />
                );
            case PieceType.Rook:
                return piece.player === Player.White ? (
                    <RookLight />
                ) : (
                    <RookDark />
                );
            case PieceType.Pawn:
                return piece.player === Player.White ? (
                    <PawnLight />
                ) : (
                    <PawnDark />
                );
            default:
                return null;
        }
    } else {
        return null;
    }
};

function ChessBoard({ id }: { id?: string | number }) {
    const [pieces, setPieces] = useState<ChessPiece[]>(startGame);
    const [selectedPiece, setSelectedPiece] = useState<ChessPiece | null>(null);
    const [selectedSquare, setSelectedSquare] = useState({ row: -1, col: -1 });
    const [playerTurn, setPlayerTurn] = useState<Player>(Player.White);
    const [history, setHistory] = useState<MoveHistory[]>([]);
    const [currentTurnNum, setCurrentTurnNum] = useState(1);

    const selectPiece = (row: number, col: number) => {
        if (
            selectedPiece &&
            selectedSquare.row === row &&
            selectedSquare.col === col
        ) {
            setSelectedPiece(null);
            setSelectedSquare({ row: -1, col: -1 });
        } else if (selectedPiece) {
            movePiece(row, col);
        } else {
            const piece = pieces.find(
                (p) => p.position.row === row && p.position.col === col,
            );
            if (piece && piece.player === playerTurn) {
                setSelectedPiece(piece || null);
                setSelectedSquare({ row, col });
            }
        }
    };

    const movePiece = (toRow: number, toCol: number) => {
        if (selectedPiece) {
            // Remove captured piece if it exists at the target location
            const capturedPiece = pieces.filter(
                (p) => p.position.row === toRow && p.position.col === toCol,
            );

            const updatedPieces = pieces.filter(
                (p) => !(p.position.row === toRow && p.position.col === toCol),
            );

            // Update the position of the selected piece
            const movedPiece = updatedPieces.map((p) =>
                p.id === selectedPiece.id
                    ? { ...p, position: { row: toRow, col: toCol } }
                    : p,
            );

            const newMove: MoveHistory = {
                id: `${currentTurnNum}-${
                    playerTurn === Player.White ? 'white' : 'black'
                }`,
                turnNum: currentTurnNum,
                currentPlayerTurn: playerTurn,
                pieceType: selectedPiece,
                fromPos: {
                    row: selectedSquare.row,
                    col: selectedSquare.col,
                },
                toPos: {
                    row: toRow,
                    col: toCol,
                },
                captured:
                    capturedPiece.length > 0 ? capturedPiece[0] : undefined,
            };

            setPieces(movedPiece);
            setSelectedPiece(null);
            setSelectedSquare({ row: -1, col: -1 });
            setHistory((prevHistory) => [...prevHistory, newMove]);
            setPlayerTurn(
                playerTurn === Player.White ? Player.Black : Player.White,
            );
            setCurrentTurnNum((prevTurnNum) =>
                playerTurn === Player.Black ? prevTurnNum + 1 : prevTurnNum,
            );

            console.log(newMove);
        }
    };

    const board = [];

    for (let col = 0; col < 8; col++) {
        const currentCol = [];
        for (let row = 0; row < 8; row++) {
            // Determine if the square should be light or dark
            const isLightColor = (row + col) % 2 === 0;
            currentCol.push(
                <ChessSquare
                    key={`${row}-${col}`}
                    row={row}
                    col={col}
                    isLightColor={isLightColor}
                    piece={renderPiece(
                        pieces.find(
                            (p) =>
                                p.position.row === row &&
                                p.position.col === col,
                        ),
                    )}
                    selectPiece={selectPiece}
                    movePiece={() => movePiece(row, col)}
                    isSelected={
                        selectedSquare.row === row && selectedSquare.col === col
                    }
                />,
            );
        }
        board.push(
            <div key={col} className='flex flex-col'>
                {currentCol}
            </div>,
        );
    }

    return (
        <div className='flex flex-col justify-center items-center'>
            <div className='p-2 flex justify-center flex-col items-center'>
                <div>
                    Current Player Turn:{' '}
                    {playerTurn === Player.White ? 'White' : 'Black'}
                </div>
                <div>Current Turn Number: {currentTurnNum}</div>
                <div className='mt-2'>
                    <Button
                        onClick={() => {
                            setPieces(startGame);
                            setPlayerTurn(Player.White);
                            setCurrentTurnNum(1);
                            setHistory([]);
                        }}
                    >
                        Restart Game
                    </Button>
                </div>
            </div>
            <div className='flex'>
                <div className='border border-black flex justify-center'>
                    {board}
                </div>
                <div className='flex flex-col'>
                    <div className='p-2 items-center justify-center'>
                        <h1 className='font-semibold'>Move History</h1>
                    </div>
                    <div>
                        {history.map((history) => {
                            return (
                                <div key={history.id}>
                                    <p>
                                        {history.turnNum}:{' '}
                                        {historyToLongNotation(history)}
                                    </p>
                                </div>
                            );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ChessBoard;
