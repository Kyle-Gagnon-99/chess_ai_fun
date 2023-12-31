/**
 * This file was auto-generated by openapi-typescript.
 * Do not make direct changes to the file.
 */


export interface paths {
  "/game/games": {
    /** Gets all games (completed and active) */
    get: operations["get_games_list_game_games_get"];
  };
  "/game/{game_id}": {
    /** Get the game with the given ID */
    get: operations["get_game_game__game_id__get"];
    /** Deletes a game by id */
    delete: operations["delete_game_game__game_id__delete"];
  };
  "/game/create": {
    /** Creates a new chess game. All pieces start in starting position */
    post: operations["create_new_game_game_create_post"];
  };
  "/game/{game_id}/reset": {
    /** Resets the game as if it was just created */
    post: operations["reset_game_game__game_id__reset_post"];
  };
  "/game/{game_id}/load_game": {
    /** Loads the game information into the backend. Typically not needed but can be used */
    post: operations["load_game_game__game_id__load_game_post"];
  };
  "/game/{game_id}/unload_game": {
    /** Removes any cache data of the current game */
    post: operations["unload_game_game__game_id__unload_game_post"];
  };
  "/game/{game_id}/game_state": {
    /** Updates the state of the game */
    post: operations["update_game_state_game__game_id__game_state_post"];
  };
  "/game/{game_id}/turn": {
    /** Updates the turn of the game. It also updates the player's turn */
    post: operations["update_turn_number_game__game_id__turn_post"];
  };
  "/game/{game_id}/move": {
    /** Moves a piece from one position to another */
    post: operations["move_game_piece_game__game_id__move_post"];
  };
  "/game/{game_id}/legal_moves": {
    /** Get the list of all legal moves */
    get: operations["get_all_legal_moves_game__game_id__legal_moves_get"];
  };
  "/game/{game_id}/pieces": {
    /** Gets all of the pieces of the game */
    get: operations["get_pieces_game__game_id__pieces_get"];
  };
}

export type webhooks = Record<string, never>;

export interface components {
  schemas: {
    /** ChessPiece */
    ChessPiece: {
      /** Id */
      id: number;
      /** String Id */
      string_id: string;
      piece_type: components["schemas"]["PieceType"];
      player: components["schemas"]["Player"];
      /** Row */
      row: number;
      /** Col */
      col: number;
      /** Game Id */
      game_id: number;
    };
    /** ChessPieceMove */
    ChessPieceMove: {
      /** Id */
      id: number;
      /** String Id */
      string_id: string;
      piece_type: components["schemas"]["PieceType"];
      player: components["schemas"]["Player"];
      /** Row */
      row: number;
      /** Col */
      col: number;
      /** Game Id */
      game_id: number;
      /** From Row */
      from_row: number;
      /** From Col */
      from_col: number;
      /** To Row */
      to_row: number;
      /** To Col */
      to_col: number;
    };
    /** Game */
    Game: {
      /** Id */
      id: number;
      /** Turn Num */
      turn_num: number;
      player_turn: components["schemas"]["Player"];
      game_state: components["schemas"]["GameState"];
      game_result: components["schemas"]["GameResult"] | null;
      /** Last En Passant */
      last_en_passant: string | null;
      /** Pieces */
      pieces: components["schemas"]["ChessPiece"][];
    };
    /**
     * GameResult
     * @enum {string}
     */
    GameResult: "White" | "Black" | "Draw" | "Stalemate";
    /**
     * GameState
     * @enum {string}
     */
    GameState: "Completed" | "Active";
    /** HTTPValidationError */
    HTTPValidationError: {
      /** Detail */
      detail?: components["schemas"]["ValidationError"][];
    };
    /** LegalMovesReponse */
    LegalMovesReponse: {
      /** Moves */
      moves: {
        [key: string]: number[][];
      };
    };
    /** MoveResponse */
    MoveResponse: {
      result: components["schemas"]["MoveResult"];
    };
    /**
     * MoveResult
     * @constant
     */
    MoveResult: "MoveIsValid";
    /**
     * PieceType
     * @enum {string}
     */
    PieceType: "Pawn" | "King" | "Queen" | "Bishop" | "Knight" | "Rook";
    /**
     * Player
     * @enum {string}
     */
    Player: "White" | "Black";
    /** ValidationError */
    ValidationError: {
      /** Location */
      loc: (string | number)[];
      /** Message */
      msg: string;
      /** Error Type */
      type: string;
    };
  };
  responses: never;
  parameters: never;
  requestBodies: never;
  headers: never;
  pathItems: never;
}

export type $defs = Record<string, never>;

export type external = Record<string, never>;

export interface operations {

  /** Gets all games (completed and active) */
  get_games_list_game_games_get: {
    parameters: {
      query?: {
        game_state?: components["schemas"]["GameState"];
        skip?: number;
        limit?: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Game"][];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get the game with the given ID */
  get_game_game__game_id__get: {
    parameters: {
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Game"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Deletes a game by id */
  delete_game_game__game_id__delete: {
    parameters: {
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Creates a new chess game. All pieces start in starting position */
  create_new_game_game_create_post: {
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Game"];
        };
      };
    };
  };
  /** Resets the game as if it was just created */
  reset_game_game__game_id__reset_post: {
    parameters: {
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Game"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Loads the game information into the backend. Typically not needed but can be used */
  load_game_game__game_id__load_game_post: {
    parameters: {
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Removes any cache data of the current game */
  unload_game_game__game_id__unload_game_post: {
    parameters: {
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": unknown;
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Updates the state of the game */
  update_game_state_game__game_id__game_state_post: {
    parameters: {
      query: {
        game_state: components["schemas"]["GameState"];
      };
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Game"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Updates the turn of the game. It also updates the player's turn */
  update_turn_number_game__game_id__turn_post: {
    parameters: {
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["Game"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Moves a piece from one position to another */
  move_game_piece_game__game_id__move_post: {
    parameters: {
      path: {
        game_id: number;
      };
    };
    requestBody: {
      content: {
        "application/json": components["schemas"]["ChessPieceMove"];
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["MoveResponse"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Get the list of all legal moves */
  get_all_legal_moves_game__game_id__legal_moves_get: {
    parameters: {
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["LegalMovesReponse"];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
  /** Gets all of the pieces of the game */
  get_pieces_game__game_id__pieces_get: {
    parameters: {
      query?: {
        player?: components["schemas"]["Player"] | null;
      };
      path: {
        game_id: number;
      };
    };
    responses: {
      /** @description Successful Response */
      200: {
        content: {
          "application/json": components["schemas"]["ChessPiece"][];
        };
      };
      /** @description Validation Error */
      422: {
        content: {
          "application/json": components["schemas"]["HTTPValidationError"];
        };
      };
    };
  };
}
