import chess
import pygame

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}
LIGHT_SQ = (232, 235, 239)
DARK_SQ = (125, 135, 150)
PIECE_NAMES = ["wp", "wR", "wN", "wB", "wK", "wQ", "bp", "bR", "bN", "bB", "bK", "bQ"]
HIGHLIGHT_COLOR = (255, 255, 0, 100)


class BoardUI:
    def __init__(self, screen):
        self.screen = screen
        self.load_images()

    def load_images(self):
        for p in PIECE_NAMES:
            img = pygame.image.load(f"assets/{p}.svg")
            IMAGES[p] = pygame.transform.smoothscale(img, (SQ_SIZE, SQ_SIZE))

    def draw_board(self):
        for r in range(DIMENSION):
            for c in range(DIMENSION):
                color = LIGHT_SQ if (r + c) % 2 == 0 else DARK_SQ
                pygame.draw.rect(
                    self.screen,
                    color,
                    pygame.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                )

    def draw_pieces(self, board):
        """Draws pieces using the python-chess board state"""
        for i in range(64):
            piece = board.piece_at(i)
            if piece:
                # python-chess counts 0-63 starting from A1 (bottom left)
                # Pygame draws from top-left (0,0)
                row = 7 - (i // 8)
                col = i % 8

                color_prefix = "w" if piece.color == chess.WHITE else "b"
                piece_type = piece.symbol().upper()
                # Map 'P' to 'p' to match your filename 'wp'
                if piece_type == "P":
                    piece_type = "p"

                asset_name = f"{color_prefix}{piece_type}"
                self.screen.blit(
                    IMAGES[asset_name],
                    pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE),
                )

    def get_square_under_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        col = mouse_pos[0] // SQ_SIZE
        row = 7 - (mouse_pos[1] // SQ_SIZE)  # Flip for python-chess
        return chess.square(col, row)

    def highlight_squares(self, board, selected_sq):
        if selected_sq is not None:
            # Create a transparent surface for the highlights
            s = pygame.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # Transparency level
            s.fill((255, 255, 0))  # Yellow

            # Get all legal moves for the selected piece
            legal_moves = [
                m.to_square for m in board.legal_moves if m.from_square == selected_sq
            ]

            for sq in legal_moves:
                row = 7 - (sq // 8)
                col = sq % 8
                self.screen.blit(s, (col * SQ_SIZE, row * SQ_SIZE))

    def draw_promotion_menu(self, color):
        """Draws a simple overlay to choose a piece using your specific asset names."""
        prefix = "w" if color == chess.WHITE else "b"
        # These match your filenames: wQ, wR, wB, wN or bQ, bR, bB, bN
        options = ["Q", "R", "B", "N"]

        # Draw a background box in the center
        menu_rect = pygame.Rect(
            WIDTH // 4, HEIGHT // 2 - SQ_SIZE // 2, WIDTH // 2, SQ_SIZE
        )
        pygame.draw.rect(self.screen, (240, 240, 240), menu_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), menu_rect, 2)

        for i, opt in enumerate(options):
            asset_name = f"{prefix}{opt}"
            self.screen.blit(
                IMAGES[asset_name], (menu_rect.x + i * SQ_SIZE, menu_rect.y)
            )

        return options
