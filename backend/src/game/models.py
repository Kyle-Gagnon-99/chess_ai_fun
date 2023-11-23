from sqlalchemy import Column, Integer, Enum as SQLAlchemyEnum, ForeignKey, String
from sqlalchemy.orm import relationship

from src.database import Base
from src.game.types import Player, GameState, GameResult, PieceType


class Game(Base):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True, autoincrement=True)
    turn_num = Column(Integer)
    player_turn = Column(SQLAlchemyEnum(Player))
    game_state = Column(SQLAlchemyEnum(GameState))
    game_result = Column(SQLAlchemyEnum(GameResult), nullable=True)
    pieces = relationship("Piece", back_populates="game")


class Piece(Base):
    __tablename__ = 'pieces'
    id = Column(Integer, primary_key=True, autoincrement=True)
    string_id = Column(String)
    piece_type = Column(SQLAlchemyEnum(PieceType))
    player = Column(SQLAlchemyEnum(Player))
    row = Column(Integer)
    col = Column(Integer)
    game_id = Column(Integer, ForeignKey('games.id'))
    game = relationship("Game", back_populates="pieces")
