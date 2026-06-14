"""数独をバックトラック法で解くサンプルです。"""

# 0 はまだ数字が入っていない空きマスを表します。
SAMPLE_SUDOKU = [
[0,0,5,3,0,0,0,0,0],
[8,0,0,0,0,0,0,2,0],
[0,7,0,0,1,0,5,0,0],
[4,0,0,0,0,5,3,0,0],
[0,1,0,0,7,0,0,0,6],
[0,0,3,2,0,0,0,8,0],
[0,6,0,5,0,0,0,0,9],
[0,0,4,0,0,0,0,3,0],
[0,0,0,0,0,9,7,0,0],
]


def is_valid_board(sudoku):
    """現在の盤面が数独のルールに違反していないか確認します。"""
    for y in range(9):
        row = [num for num in sudoku[y] if num != 0]
        if len(row) != len(set(row)):
            return False

    for x in range(9):
        col = [sudoku[y][x] for y in range(9) if sudoku[y][x] != 0]
        if len(col) != len(set(col)):
            return False

    for block_y in range(0, 9, 3):
        for block_x in range(0, 9, 3):
            block = []
            for y in range(block_y, block_y + 3):
                for x in range(block_x, block_x + 3):
                    if sudoku[y][x] != 0:
                        block.append(sudoku[y][x])
            if len(block) != len(set(block)):
                return False

    return True


def get_usable_nums(pos,sudoku):
    """指定したマスに入れられる数字のリストを返します。"""
    # pos は [y, x] の順で、y が行、x が列です。
    block_x = pos[1]//3 * 3
    block_y = pos[0]//3 * 3

    # 同じ行、同じ列、同じ 3x3 ブロックにある数字を集めます。
    row = set(sudoku[pos[0]])
    col = {line[pos[1]] for line in sudoku}
    block = set(sum([line[block_x:block_x+3] for line in sudoku][block_y:block_y+3],[]))

    # 1 から 9 のうち、すでに使われている数字を除いたものが候補です。
    usable_nums = list(set(range(1,10)) - (row|col|block))

    return usable_nums


def solve_sudoku(sudoku,x=0,y=0):
    """バックトラック法で数独を解きます。"""
    if y > 8: # yが8より大きい = すべてのマスに数字を配置した状態
        return True
    elif sudoku[y][x] != 0: # 空きマスじゃないとき
        if x == 8: # xが8 = その行のすべてのマスに数字を配置した状態
            if solve_sudoku(sudoku, 0, y+1): # 次の行の先頭から見ていく
                return True
        else:
            if solve_sudoku(sudoku, x+1, y): # 次の列を見る
                return True
    else: # 空きマスのとき
        for num in get_usable_nums([y,x],sudoku): # 入力できる数字を順に入れていく
            sudoku[y][x] = num
            if x == 8:
                if solve_sudoku(sudoku,0,y+1):
                    return True
            else:
                if solve_sudoku(sudoku,x+1,y):
                    return True
        # 候補をすべて試しても解けない場合は、マスを空に戻して前のマスへ戻ります。
        sudoku[y][x] = 0
        return False
        

def show_sudoku(sudoku):
    """数独の盤面を 1 行ずつ表示します。"""
    for line in sudoku:
        print(line)


if __name__ == "__main__":
    sudoku = [row[:] for row in SAMPLE_SUDOKU]
    solve_sudoku(sudoku)
    show_sudoku(sudoku)
