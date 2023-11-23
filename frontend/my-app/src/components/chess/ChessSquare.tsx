import React, { ReactNode } from 'react';

function ChessSquare({
    row,
    col,
    isLightColor,
    piece,
    selectPiece,
    movePiece,
    isSelected,
}: {
    row: number;
    col: number;
    isLightColor?: boolean;
    piece?: ReactNode;
    selectPiece: (row: number, col: number) => void;
    movePiece: (row: number, col: number) => void;
    isSelected: boolean;
}) {
    const squareClasses = `w-16 h-16 flex justify-center items-center`;
    const lightClass = `bg-sandcastle-light ${squareClasses}`;
    const darkClass = `bg-sandcastle-dark ${squareClasses}`;
    const highlightClass = `bg-green-200 ${squareClasses}`;

    const handleClick = () => {
        if (piece) {
            selectPiece(row, col);
        } else {
            movePiece(row, col);
        }
    };

    let className = isLightColor ? lightClass : darkClass;
    if (isSelected) {
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
