from random import choice, randint
from textwrap import dedent


MARKS = ['✕', '◯']

ALL_PATHS = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6],
    [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
]

CHECK_MAP = {
    '1': [[0, 1, 2], [0, 3, 6], [0, 4, 8]],
    '2': [[0, 1, 2], [1, 4, 7]],
    '3': [[0, 1, 2], [2, 5, 8], [2, 4, 6]],
    '4': [[0, 3, 6], [3, 4, 5]],
    '5': [[1, 4, 7], [3, 4, 5], [0, 4, 8], [2, 4, 6]],
    '6': [[2, 5, 8], [3, 4, 5]],
    '7': [[0, 3, 6], [6, 7, 8], [2, 4, 6]],
    '8': [[1, 4, 7], [6, 7, 8]],
    '9': [[6, 7, 8], [2, 5, 8], [0, 4, 8]]
}


def check_winning_turn(board: list[str], mark: str) -> str | None:
    for path in ALL_PATHS:
        two_marks_in_path = [
            item == mark for item in [board[cell] for cell in path]
        ].count(True) == 2
        path_cells_emptiness = [
            item == ' ' for item in [board[cell] for cell in path]
        ]
        if two_marks_in_path and path_cells_emptiness.count(True) == 1:
            return str(path[path_cells_emptiness.index(True)] + 1)


def apply_turn(
    turn: str, mark: str, board: list[str], available_turns: list[str]
) -> None:
    board[int(turn) - 1] = mark
    available_turns.remove(turn)


def get_user_turn(available_turns: list[str]) -> str:
    while True:
        user_input = input('Your turn (Enter a number or q to quit): ')
        if user_input == 'q':
            exit(0)
        elif user_input not in available_turns:
            print('Incorrect input. Try again.')
        else:
            return user_input


def get_cpu_turn(
    board: list[str], available_turns: list[str], cpu_mark: str, user_mark: str
) -> str:
    winning_turn = check_winning_turn(board, cpu_mark)
    if winning_turn:
        return winning_turn
    else:
        loss_preventing_turn = check_winning_turn(board, user_mark)
        if loss_preventing_turn:
            return loss_preventing_turn
    return choice(available_turns)


def show_board(board: list[str]) -> None:
    print(dedent(
        f'''\
            ┌───┬───┬───┐  ┌───┬───┬───┐
            │ {board[0]} │ {board[1]} │ {board[2]} │  │ 1 │ 2 │ 3 │
            ├───┼───┼───┤  ├───┼───┼───┤
            │ {board[3]} │ {board[4]} │ {board[5]} │  │ 4 │ 5 │ 6 │
            ├───┼───┼───┤  ├───┼───┼───┤
            │ {board[6]} │ {board[7]} │ {board[8]} │  │ 7 │ 8 │ 9 │
            └───┴───┴───┘  └───┴───┴───┘\
        '''
    ))


def check_win(mark: str, last_turn: str, board: list[str]) -> bool | None:
    paths_to_check = CHECK_MAP[last_turn]
    for path in paths_to_check:
        if all([item == mark for item in [board[cell] for cell in path]]):
            return True


def main() -> None:
    while True:
        board = [' '] * 9
        available_turns = [str(num) for num in range(1, 10)]
        user_mark = MARKS[randint(0, 1)]
        cpu_mark = MARKS[not MARKS.index(user_mark)]

        for iteration in range(5):
            if user_mark == '✕':
                show_board(board)
                turn = get_user_turn(available_turns)
                apply_turn(turn, user_mark, board, available_turns)
                if iteration > 1 and check_win(user_mark, turn, board):
                    show_board(board)
                    print('You won!\n----------------------------')
                    break
                if iteration < 4:
                    turn = get_cpu_turn(
                        board, available_turns, cpu_mark, user_mark
                    )
                    apply_turn(turn, cpu_mark, board, available_turns)
                    if check_win(cpu_mark, turn, board):
                        show_board(board)
                        print('CPU won!\n----------------------------')
                        break
            else:
                turn = get_cpu_turn(
                    board, available_turns, cpu_mark, user_mark
                )
                apply_turn(turn, cpu_mark, board, available_turns)
                if iteration > 1 and check_win(cpu_mark, turn, board):
                    show_board(board)
                    print('CPU won!\n----------------------------')
                    break
                if iteration < 4:
                    show_board(board)
                    turn = get_user_turn(available_turns)
                    apply_turn(turn, user_mark, board, available_turns)
                    if check_win(user_mark, turn, board):
                        show_board(board)
                        print('You won!\n----------------------------')
                        break
            if iteration == 4:
                show_board(board)
                print('Draw!\n----------------------------')


if __name__ == '__main__':
    main()
