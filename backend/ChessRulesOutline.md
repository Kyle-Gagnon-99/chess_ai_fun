# Chess Rules Outline

Here is an outline possibly of what to do to validate chess rules

## Outline

### Movement Rules

-   Pawn:

    -   Movement:
        -   It can only move forward
    -   Number of Spaces:
        -   On its opening move it can move either one or two spaces
        -   Otherwise it can only move one
    -   Capturing:
        -   A pawn can capture an enemy piece if it is diagonally forward one space on either side
    -   Movement Restrictions:
        -   It can not jump any friendly or enemy pieces

-   Rook:

    -   Movement:
        -   It can move forward / backward / left / right
    -   Number of Spaces:
        -   It can move any number of available spaces in one direction
        -   If a friendly piece is in that direction, it can not move past it or jump it
    -   Capturing:
        -   A rook can capture an enemy piece in its path
    -   Movement Restrictions:
        -   It can not jump any friendly or enemy pieces
        -   It can only move in one direction per move

-   Bishop

    -   Movement:
        -   It can move diagonally, forward or backward
        -   The diagonal can be the left or right diagonal
    -   Number of Spaces:
        -   It can move any number of available spaces in one direction
        -   If a friendly piece is in that direction, it can not move past it or jump it
    -   Capturing:
        -   A bishop can capture an enemy piece in its path
    -   Movement Restrictions:
        -   It can not jump any friendly or enemy pieces
        -   It can only move in one direction per move

-   Knight

    -   Movement:
        -   It can move in an L shape
            -   The L shape is defined as two spaces on one axis and one space on the other axis
            -   Diagonals are not allowed
            -   The two spaces can be on the same axis
            -   I.E. it can move two spaces forward and one space left
        -   It can move forward / backward in the L shape
    -   Number of Spaces:
        -   It can move two spaces in one direction and one space in the other direction
        -   It can move one space in one direction and two spaces in the other direction
    -   Capturing:
        -   A knight can capture an enemy piece that it lands on
    -   Movement Restrictions:
        -   It can jump over friendly or enemy pieces

-   Queen

    -   Movement:
        -   It can move forward / backward / left / right
        -   It can move diagonally, forward or backward
    -   Number of Spaces:
        -   It can move any number of available spaces in one direction
        -   If a friendly piece is in that direction, it can not move past it or jump it
    -   Capturing:
        -   A queen can capture an enemy piece in its path
    -   Movement Restrictions:
        -   It can not jump any friendly or enemy pieces
        -   It can only move in one direction per move

-   King
    -   Movement:
        -   It can move forward / backward / left / right
        -   It can move diagonally, forward or backward
    -   Number of Spaces:
        -   It can move one space in any direction
    -   Capturing:
        -   A king can capture an enemy piece in its path
    -   Movement Restrictions:
        -   It can not jump any friendly or enemy pieces
        -   It can only move in one direction per move
        -   It can not move into a space that is under attack by an enemy piece (a.k.a if a piece can capture it on its next move)
        -   It must move out of check if it is in check (a.k.a if a piece can capture it on its next move)

### Special Movement Rules

-   Castling
    A castle is when the king and rook move in a special way to protect the king. There are two types of castles, kingside and queenside. The king and rook can only castle if the following conditions are met:

    -   The king and rook have not moved yet
    -   There are no pieces between the king and rook
    -   The king is not in check
    -   The king does not move through a space that is under attack by an enemy piece
    -   The king does not end up in check

    Kingside Castle:

    -   The king moves two spaces towards the rook on the kingside (the side with the king)
    -   The rook moves to the space on the other side of the king

    Queenside Castle:

    -   The king moves two spaces towards the rook on the queenside (the side without the king)
    -   The rook moves to the space on the other side of the king

-   En Passant
    En Passant is a special move that a pawn can make if it is next to an enemy pawn that just moved two spaces on its opening move. The pawn can move diagonally behind the enemy pawn and capture it as if it only moved one space. The enemy pawn is removed from the board.

-   Pawn Promotion
    If a pawn reaches the other side of the board, it can be promoted to any other piece except for a king or pawn. The pawn is removed from the board and the new piece is placed on the board.

### Game Conditions

A game condition is when the game exists in one of these states besides a "normal" state where a game can still go on. If any of these conditions are met, the game is over.

-   Check

    A king is in check if an enemy piece can capture it on its next move. The king must move out of check if it is in check.

-   Checkmate

    A king is in checkmate if it is in check and it can not move out of check. The game is over and the player who put the king in checkmate wins.

-   Stalemate

    A stalemate is when a player can not make a legal move but their king is not in check. The game is over and the game is a draw.

-   Draw

    A draw is when the game ends in a tie. This can happen in the following ways:

    -   The game ends in a stalemate
    -   The same position is repeated three times
    -   There have been 50 moves without a pawn being moved or a piece being captured

### Special Rules

When a King is in check the player who has their King in check must do one of the following to remove the King from check:

-   Move the King out of check (the King can not move into a space that is under attack by an enemy piece)
-   Capture the piece that is putting the King in check
-   Block the piece that is putting the King in check with another piece

If the player who has their King in check can not do any of the above, then the King is in checkmate and the game is over.

# Code Suggestions

## Validation A Move

In the beginning of the game, for each piece get the list of valid spaces. Do this by

1. For each owned piece add to a hash that identifies the list of all owned pieces. All pieces have an ID (white-pawn-4, black-queen, black-bishop-1, white-knight-1)
2. Valid Spaces Method

-   First create the hash of all spaces that the piece could go if there are no special rules and no friendly or enemy spaces blocking it
-   Then go through each piece again and for each valid space, check if a friendly is there and remove the space
-   Depending on the piece remove any space
