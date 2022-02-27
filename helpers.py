def board_to_string(board, win = False):
    line_sep = "\n\n"
    str_board = ["#" if sq!=sq else "X" if sq else "O" for sq in board]
    if win:
        str_board = [f"**{str_board[i]}**" if i in win else str_board[i] for i in range(9)]

    return f"|\t{str_board[0]}\t|\t{str_board[1]}\t|\t{str_board[2]}\t|{line_sep}|\t{str_board[3]}\t|\t{str_board[4]}\t|\t{str_board[5]}\t|{line_sep}|\t{str_board[6]}\t|\t{str_board[7]}\t|\t{str_board[8]}\t|"

def has_won(board):
    win_states = [  [0, 1, 2],
                    [3, 4, 5],
                    [6, 7, 8],
                    [0, 3, 6],
                    [1, 4, 7],
                    [2, 5, 8],
                    [0, 4, 8],
                    [2, 4, 6]]
    for state in win_states:
        if all(board[index]==board[state[0]] for index in state):
            return state
    return None
