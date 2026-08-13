import pygame
import chess

# Window settings
WIDTH, HEIGHT = 700, 700
SQ_SIZE = WIDTH // 8

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Python Chess")

WHITE = (240, 217, 181)
BROWN = (181, 136, 99)
BLUE = (0, 0, 255)

font = pygame.font.SysFont("Segoe UI Symbol", 48)

board = chess.Board()

pieces = {
    "P": "♙",
    "N": "♘",
    "B": "♗",
    "R": "♖",
    "Q": "♕",
    "K": "♔",
    "p": "♟",
    "n": "♞",
    "b": "♝",
    "r": "♜",
    "q": "♛",
    "k": "♚",
}

selected_square = None


def draw_board():
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(
                screen,
                color,
                (col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE),
            )

    if selected_square is not None:
        file = chess.square_file(selected_square)
        rank = chess.square_rank(selected_square)
        pygame.draw.rect(
            screen,
            BLUE,
            (
                file * SQ_SIZE,
                (7 - rank) * SQ_SIZE,
                SQ_SIZE,
                SQ_SIZE,
            ),
            4,
        )


def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            file = chess.square_file(square)
            rank = chess.square_rank(square)

            text = font.render(pieces[piece.symbol()], True, (0, 0, 0))

            screen.blit(
                text,
                (
                    file * SQ_SIZE + 15,
                    (7 - rank) * SQ_SIZE + 10,
                ),
            )


running = True

while running:
    draw_board()
    draw_pieces()

    pygame.display.flip()

    if board.is_checkmate():
        print("Checkmate!")
        running = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            x, y = pygame.mouse.get_pos()

            file = x // SQ_SIZE
            rank = 7 - (y // SQ_SIZE)

            square = chess.square(file, rank)

            if selected_square is None:

                piece = board.piece_at(square)

                if piece and piece.color == board.turn:
                    selected_square = square

            else:

                move = chess.Move(selected_square, square)

                if move in board.legal_moves:
                    board.push(move)

                else:
                    # Promotion
                    promotion = chess.Move(
                        selected_square,
                        square,
                        promotion=chess.QUEEN,
                    )

                    if promotion in board.legal_moves:
                        board.push(promotion)

                selected_square = None

pygame.quit()