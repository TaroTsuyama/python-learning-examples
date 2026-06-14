import json
from numpy import random as rnd

def read_json(path):
    """JSON ファイルを読み込み、Python のデータとして返します。"""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def input_int(message, max, min):
    """min から max までの整数が入力されるまで、入力を繰り返します。"""
    while True:
        ip_data = input(message)

        try:
            int_data = int(ip_data)

            if int_data in range(min,max+1):
                return int_data

            else:
                print("数値の範囲が不正です。")

        except:
            print("数値で入力してください。")

def quiz(num=10):
    """
        引数 num
            デフォルト値10 この関数を呼ぶときに引数を指定しないと、この値が適用される
    """

    json_file = "quiz.json"
    quiz_list = read_json(json_file)
    rnd.shuffle(quiz_list)

    # 指定された出題数が問題数より多い場合は、問題数に合わせます。
    if len(quiz_list) < num:
        num = len(quiz_list)

    correct = 0
    for _ in range(num):
        # シャッフル済みの問題リストから、1 問ずつ取り出します。
        quiz_data = quiz_list.pop()

        # 難易度は 0 から 5 の範囲に収めます。
        difficulty = min(max(quiz_data["Difficulty"], 0), 5)

        # 難易度を星で表示するための文字列を作ります。
        stars = f"(難易度{'★' * difficulty}{'☆' * (5 - difficulty)})"

        question = quiz_data["Qestion"]
        choices = quiz_data["Choices"]
        # 選択肢をシャッフルする前に、正解の文字列を保存しておきます。
        answer = choices[quiz_data["Answer"]]
        rnd.shuffle(choices)

        print(question)
        print(stars)
        for i in range(len(choices)):
            # 画面には 1 から始まる番号で選択肢を表示します。
            print(i+1, choices[i])

        # リストの要素番号は 0 から始まるため、入力値から 1 を引きます。
        selection = input_int(":", len(choices), 1) - 1 

        if choices[selection] == answer:
            print("正解\n")
            correct += 1
        else:
            print("不正解\n")

    # 正解数と正答率を表示
    print(f"{num} 問中 {correct} 問正解しました。(正答率:{int(correct/num*100)}%)")

quiz(10)
