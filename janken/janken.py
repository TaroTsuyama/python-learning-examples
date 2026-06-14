from numpy import random as rnd

# プレイヤーと PC が選べる手をタプルで定義します。
HANDS = ("グー","チョキ","パー")

# 「左の手」は「右の手」に勝つ、という対応表です。
WIN_PATTERN = {
    "グー" : "チョキ",
    "チョキ" : "パー",
    "パー" : "グー"
}

def user_select():
    """ユーザーの入力を受け取り、対応する手を返します。"""
    ip = input_int(message=":", min=1, max=3) - 1

    return HANDS[ip]

def random_select():
    """PC の手をランダムに選びます。"""
    tmp_list = list(HANDS)
    rnd.shuffle(tmp_list)

    return(tmp_list[0])

def input_int(message, min, max):
    """min から max までの整数が入力されるまで、入力を繰り返します。"""
    while True:
        ip_data = input(message)

        if ip_data.isdecimal():
            int_data = int(ip_data)
            if int_data in range(min, max+1):
                return int_data
            else:
                print("数値の範囲が不正です。")

        else:
            print("数値で入力してください。")

def main():
    print("\nじゃんけんをします。対応する数字を入力してください。")
    for num, hand in enumerate(HANDS,start=1):
        print(num, hand)

    # 10 回勝負を行い、勝った回数を数えます。
    janken_num = 10
    win = 0
    for _ in range(janken_num):
        # flg は「あいこ」になった後の掛け声を切り替えるために使います。
        flg = True
        while True:
            if flg:
                message = ("\nじゃんけん・・・","ぽん！")
            else:
                message = ("\nあーいこーで・・・","しょっ！")

            print(message[0])

            user_hand = user_select()
            pc_hand = random_select()

            print(message[1])

            print(f"(あなた){user_hand} : (PC){pc_hand}")

            # 勝ち、あいこ、負けの順に判定します。
            if WIN_PATTERN[user_hand] == pc_hand:
                win += 1
                print("あなたのかち")
                break

            elif user_hand == pc_hand:
                flg = False

            else:
                print("あなたのまけ")
                break

    print(f"\n{'=' * 20}\n{win}勝{janken_num - win}敗\n")

main()
