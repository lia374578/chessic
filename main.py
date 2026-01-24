import chess
import pygame
from board_ui import BoardUI
from engine import GameEngine

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
LIGHT_SQ = (232, 235, 239)
DARK_SQ = (125, 135, 150)
PIECE_NAMES = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
HIGHLIGHT_COLOR = (255, 255, 0, 100)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    ge = GameEngine()
    ui = BoardUI(screen)

    selected_sq = None
    promotion_move = None

    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            elif e.type == pygame.MOUSEBUTTONDOWN:
                if promotion_move:
                    # Handle promotion selection
                    mouse_pos = pygame.mouse.get_pos()
                    # Check which piece in the menu was clicked
                    # (Simple logic: menu starts at WIDTH//4, each icon is SQ_SIZE)
                    menu_x_start = WIDTH // 4
                    if (
                        HEIGHT // 2 - SQ_SIZE // 2
                        <= mouse_pos[1]
                        <= HEIGHT // 2 + SQ_SIZE // 2
                    ):
                        idx = (mouse_pos[0] - menu_x_start) // SQ_SIZE
                        pieces = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
                        if 0 <= idx < 4:
                            move = chess.Move(
                                promotion_move[0],
                                promotion_move[1],
                                promotion=pieces[idx],
                            )
                            ge.board.push(move)
                            promotion_move = None
                else:
                    sq = ui.get_square_under_mouse()
                    if selected_sq == sq:
                        selected_sq = None
                    elif selected_sq is None:
                        if ge.board.piece_at(sq):
                            selected_sq = sq
                    else:
                        if ge.is_promotion_move(selected_sq, sq):
                            # Check if the move is even legal before triggering menu
                            test_move = chess.Move(selected_sq, sq, chess.QUEEN)
                            if test_move in ge.board.legal_moves:
                                promotion_move = (selected_sq, sq)
                        else:
                            move = chess.Move(selected_sq, sq)
                            if move in ge.board.legal_moves:
                                ge.board.push(move)
                        selected_sq = None

        ui.draw_board()
        ui.highlight_squares(ge.board, selected_sq)
        ui.draw_pieces(ge.board)

        if promotion_move:
            ui.draw_promotion_menu(ge.board.turn)

        pygame.display.flip()
        clock.tick(MAX_FPS)


if __name__ == "__main__":
    main()
