"""ブラウザから使える数独ソルバーです。

実行方法:
    python app.py

ブラウザで http://127.0.0.1:5000 を開くと、数独の盤面を入力できます。
"""

from flask import Flask, render_template_string, request

from sudoku_solver import SAMPLE_SUDOKU, is_valid_board, solve_sudoku


app = Flask(__name__)

HTML = """
<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>数独ソルバー</title>
  <style>
    body {
      font-family: system-ui, sans-serif;
      margin: 32px;
      color: #222;
      background: #f6f7f9;
    }
    main {
      max-width: 560px;
      margin: 0 auto;
    }
    h1 {
      font-size: 28px;
      margin-bottom: 8px;
    }
    p {
      line-height: 1.7;
    }
    .board {
      display: grid;
      grid-template-columns: repeat(9, 44px);
      grid-template-rows: repeat(9, 44px);
      margin: 24px 0;
      width: 396px;
      border: 3px solid #222;
      background: #222;
    }
    input {
      width: 44px;
      height: 44px;
      box-sizing: border-box;
      border: 1px solid #aaa;
      text-align: center;
      font-size: 22px;
      font-weight: 700;
      background: white;
    }
    input:focus {
      outline: 3px solid #6aa8ff;
      position: relative;
      z-index: 1;
    }
    .given {
      background: #fff2d6;
    }
    .solved {
      color: #0b5cad;
    }
    .right-border {
      border-right: 3px solid #222;
    }
    .bottom-border {
      border-bottom: 3px solid #222;
    }
    .buttons {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    button, a.button {
      border: 0;
      padding: 10px 16px;
      color: white;
      background: #222;
      border-radius: 6px;
      font-size: 16px;
      text-decoration: none;
      cursor: pointer;
    }
    a.button {
      background: #666;
    }
    .message {
      padding: 12px 14px;
      border-radius: 6px;
      background: #fff;
      border-left: 5px solid #d33;
    }
  </style>
</head>
<body>
  <main>
    <h1>数独ソルバー</h1>
    <p>空欄はそのままにして、分かっている数字だけ入力してください。解くボタンを押すと Python が答えを計算します。</p>

    {% if message %}
      <p class="message">{{ message }}</p>
    {% endif %}

    <form method="post">
      <div class="board">
        {% for y in range(9) %}
          {% for x in range(9) %}
            {% set value = board[y][x] %}
            {% set class_name = "" %}
            {% if x in [2, 5] %}
              {% set class_name = class_name + " right-border" %}
            {% endif %}
            {% if y in [2, 5] %}
              {% set class_name = class_name + " bottom-border" %}
            {% endif %}
            {% if value != 0 and solved %}
              {% set class_name = class_name + " solved" %}
            {% endif %}
            <input
              class="{{ class_name }}"
              type="text"
              name="cell_{{ y }}_{{ x }}"
              value="{{ "" if value == 0 else value }}"
              maxlength="1"
              inputmode="numeric"
              pattern="[1-9]"
              autocomplete="off"
            >
          {% endfor %}
        {% endfor %}
      </div>
      <div class="buttons">
        <button type="submit">解く</button>
        <a class="button" href="/">リセット</a>
      </div>
    </form>
  </main>
</body>
</html>
"""


def read_board_from_form(form):
    """フォームに入力された81マスを、9x9のリストに変換します。"""
    board = []
    for y in range(9):
        row = []
        for x in range(9):
            value = form.get(f"cell_{y}_{x}", "").strip()
            row.append(int(value) if value else 0)
        board.append(row)
    return board


@app.route("/", methods=["GET", "POST"])
def index():
    """数独の入力画面を表示し、POST時は解答を計算します。"""
    message = ""
    solved = False

    if request.method == "POST":
        try:
            board = read_board_from_form(request.form)
        except ValueError:
            board = [[0 for _ in range(9)] for _ in range(9)]
            message = "1から9までの数字だけを入力してください。"
        else:
            if not is_valid_board(board):
                message = "同じ行・列・3x3ブロックに同じ数字があります。"
            else:
                solved_board = [row[:] for row in board]
                if solve_sudoku(solved_board):
                    board = solved_board
                    solved = True
                    message = "解答を表示しました。"
                else:
                    message = "この盤面は解けませんでした。"
    else:
        board = [row[:] for row in SAMPLE_SUDOKU]

    return render_template_string(
        HTML,
        board=board,
        message=message,
        solved=solved,
    )


if __name__ == "__main__":
    app.run(debug=True)
