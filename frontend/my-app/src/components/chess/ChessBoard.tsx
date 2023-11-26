'use client';
import React, { useEffect, useState } from 'react';
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
import { components } from '@/lib/openapi';
import { GET, POST } from '@/lib/apiClient';

function renderPiece(piece: components['schemas']['ChessPiece'] | undefined) {
    if (piece) {
        const pieceType = piece.piece_type;

        switch (pieceType) {
            case 'Bishop':
                return piece.player === 'White' ? (
                    <BishopLight />
                ) : (
                    <BishopDark />
                );
            case 'Rook':
                return piece.player === 'White' ? <RookLight /> : <RookDark />;
            case 'Knight':
                return piece.player === 'White' ? (
                    <KnightLight />
                ) : (
                    <KnightDark />
                );
            case 'King':
                return piece.player === 'White' ? <KingLight /> : <KingDark />;
            case 'Queen':
                return piece.player === 'White' ? (
                    <QueenLight />
                ) : (
                    <QueenDark />
                );
            case 'Pawn':
                return piece.player === 'White' ? <PawnLight /> : <PawnDark />;
            default:
                return undefined;
        }
    } else {
        return undefined;
    }
}

function ChessBoard({ id }: { id: string | number }) {
    // Keeps track of the overall game state
    const [gameState, setGameState] = useState<
        components['schemas']['Game'] | undefined
    >(undefined);

    // In case of any errors
    const [error, setError] = useState<
        components['schemas']['HTTPValidationError'] | undefined
    >();

    // The list of pieces from the game
    const [pieces, setPieces] = useState<
        components['schemas']['Game']['pieces']
    >([]);

    // Keeps track of the current legal moves
    const [legalMoves, setLegalMoves] = useState<
        components['schemas']['LegalMovesReponse'] | undefined
    >();

    // Keep track of the current player's turn
    const [currentPlayerTurn, setCurrentPlayerTurn] = useState<
        components['schemas']['Player'] | undefined
    >();

    // Keep track of the current turn number
    const [currentTurnNum, setCurrentTurnNum] = useState(1);

    // Keep track of the currently selected piece
    const [selectedPiece, setSelectedPiece] = useState<
        components['schemas']['ChessPiece'] | null | undefined
    >(null);

    /**
     * Fetch the game state of the currently given ID
     * @param id The ID of the game to get
     */
    const fetchGameState = async (id: string | number) => {
        // Convert the id to a number if needed
        const id_num = Number(id);

        // Grab the game state
        const { data, error } = await GET('/game/{game_id}', {
            params: {
                path: {
                    game_id: id_num,
                },
            },
        });

        if (error) {
            setError(error);
        }

        setGameState(data);
    };

    /**
     * Retreives all legal moves from the backend's cache
     * @param id The ID of the game to get the legal moves of
     */
    const fetchLegalMoves = async (id: string | number) => {
        // Conver the id to a number if needed
        const id_num = Number(id);

        // Grab the legal moves
        const { data, error } = await GET('/game/{game_id}/legal_moves', {
            params: {
                path: {
                    game_id: id_num,
                },
            },
        });

        if (error) {
            setError(error);
        }

        setLegalMoves(data);
    };

    // Sets the game state upon component mount
    useEffect(() => {
        fetchGameState(id);
    }, []);

    // Whenever the game state is updated, update the pieces
    useEffect(() => {
        console.log(gameState);
        if (gameState) {
            setPieces(gameState.pieces);
            fetchLegalMoves(id);
            setCurrentPlayerTurn(gameState.player_turn);
            setCurrentTurnNum(gameState.turn_num);
        }
    }, [gameState]);

    const selectedPiceMoves = selectedPiece
        ? legalMoves?.moves[selectedPiece.string_id]
        : [];

    /**
     * Resets the game, moves all pieces back to their starting positions
     */
    const resetGame = async () => {
        const { data, error } = await POST('/game/{game_id}/reset', {
            params: {
                path: {
                    game_id: Number(id),
                },
            },
        });

        if (error) {
            console.log(error);
        }

        setGameState(data);
    };

    const updateTurn = async () => {
        const { data, error } = await POST('/game/{game_id}/turn', {
            params: {
                path: {
                    game_id: Number(id),
                },
            },
        });

        if (data) {
            setGameState(data);
        }
    };

    // Gives logic to currently select a piece
    const selectPiece = (col: number, row: number) => {
        const piece = pieces.find((p) => p.row === row && p.col === col);

        // If the same square is selected, then deselect it
        setSelectedPiece((prevVal) => {
            if (prevVal && prevVal.col === col && prevVal.row === row) {
                return null;
            } else {
                return piece;
            }
        });
    };

    const movePiece = async (toCol: number, toRow: number) => {
        if (selectedPiece) {
            console.log(`Attempting to move to ${toCol},${toRow}`);
            const { error } = await POST('/game/{game_id}/move', {
                params: {
                    path: {
                        game_id: Number(id),
                    },
                },
                body: {
                    id: selectedPiece.id,
                    string_id: selectedPiece.string_id,
                    piece_type: selectedPiece.piece_type,
                    player: selectedPiece.player,
                    row: selectedPiece.row,
                    col: selectedPiece.col,
                    game_id: Number(id),
                    from_row: selectedPiece.row,
                    from_col: selectedPiece.col,
                    to_row: toRow,
                    to_col: toCol,
                },
            });

            if (error) {
                console.log('Nope you cant do that');
            }

            selectedPiece.row = toRow;
            selectedPiece.col = toCol;
            updateTurn();
            setSelectedPiece(undefined);
        }
    };

    const board: React.JSX.Element[] = [];
    let trueCol = 0;

    // Construct the board
    for (let col = 0; col < 8; col++) {
        trueCol = trueCol + 1;
        let trueRow = 9;
        const currentCol = [];
        for (let row = 0; row < 8; row++) {
            trueRow = trueRow - 1;
            // Determine if the square should be light or dark
            const isLightColor = (row + col) % 2 === 0;
            currentCol.push(
                <ChessSquare
                    key={`${row}-${col}`}
                    row={trueRow}
                    col={trueCol}
                    isLightColor={isLightColor}
                    piece={renderPiece(
                        pieces.find(
                            (p) => p.row === trueRow && p.col === trueCol,
                        ),
                    )}
                    selectPiece={selectPiece}
                    movePiece={movePiece}
                    selectedPiece={selectedPiece}
                    legalMovesForSelectedPiece={selectedPiceMoves}
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
        <div className='flex flex-col justify-center items-center gap-3'>
            <div>
                <h1 className='font-semibold text-4xl'>Game {id}</h1>
            </div>
            <div className='flex flex-col m-3 gap-3'>
                <h2 className='font-semibold text-xl'>Game Controls</h2>
                <div className='flex flex-row justify-center items-center'>
                    <Button onClick={() => resetGame()}>Reset Game</Button>
                </div>
            </div>
            <div className='flex'>
                <div className='border border-black flex justify-center'>
                    {board}
                </div>
            </div>
        </div>
    );
}

export default ChessBoard;
