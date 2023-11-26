import { components } from '@/lib/openapi';
import React, { ReactNode } from 'react';

function ChessSquare({
    row,
    col,
    isLightColor,
    piece,
    selectPiece,
    movePiece,
    selectedPiece,
    legalMovesForSelectedPiece,
}: {
    row: number;
    col: number;
    isLightColor?: boolean;
    piece?: ReactNode;
    selectPiece: (col: number, row: number) => void;
    movePiece: (col: number, row: number) => void;
    selectedPiece?: components['schemas']['ChessPiece'] | null;
    legalMovesForSelectedPiece: number[][] | undefined;
}) {
    const squareClasses = `w-16 h-16 flex justify-center items-center`;
    const lightClass = `bg-sandcastle-light ${squareClasses}`;
    const darkClass = `bg-sandcastle-dark ${squareClasses}`;
    const highlightClass = `bg-green-200 ${squareClasses} border border-green-700`;

    const isLegalMove = legalMovesForSelectedPiece?.some(
        ([legalCol, legalRow]) => legalRow === row && legalCol === col,
    );

    const handleClick = () => {
        if (piece) {
            selectPiece(col, row);
        } else {
            movePiece(col, row);
        }
    };

    let className = isLightColor ? lightClass : darkClass;
    if (
        selectedPiece &&
        selectedPiece.row === row &&
        selectedPiece.col === col
    ) {
        className = highlightClass;
    } else if (isLegalMove) {
        className = highlightClass;
    }

    return (
        <div className={className} onClick={handleClick}>
            {piece && (
                <div className='w-16 h-16 justify-center flex'>{piece}</div>
            )}
        </div>
    );
}

export default ChessSquare;
