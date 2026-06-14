#coding: utf-8
"""pygame-ce を使った簡単なシューティングゲームのサンプルです。"""

import pygame
from pygame.locals import *
import sys
import numpy as np
from enum import Enum, auto

# 画面サイズや描画で使う色など、ゲーム全体で共有する設定です。
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 600
SCREEN_RECT = Rect(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
SHADOW_OFFSET = (10,10)
SHADOW_COLOR = pygame.Color(0,0,0,100)
FLICKER_COLOR = pygame.Color(255,0,0,240)

# 画像ファイルと、プレイヤー・敵キャラクターの基本データです。
IMAGE_DIR = "img/"
PLAYER_DATA = {"name":"heisha", "img":"heisha.png", "score":0, "speed":5, "life":3}
ENEMIES_DATA = (
    {"name":"adidas", "img":"adidas.png", "score":100, "speed":5, "life":5},
    {"name":"amazon", "img":"amazon.png", "score":100, "speed":5, "life":5},
    {"name":"apple", "img":"apple.png", "score":100, "speed":5, "life":5},
    {"name":"burgerking", "img":"burgerking.png", "score":100, "speed":5, "life":5},
    {"name":"cocacola", "img":"cocacola.png", "score":100, "speed":5, "life":5},
    {"name":"ebay", "img":"ebay.png", "score":100, "speed":5, "life":5},
    {"name":"facebook", "img":"facebook.png", "score":100, "speed":5, "life":5},
    {"name":"google", "img":"google.png", "score":5000, "speed":15, "life":15},
    {"name":"hp", "img":"hp.png", "score":100, "speed":5, "life":5},
    {"name":"huawei", "img":"huawei.png", "score":100, "speed":5, "life":5},
    {"name":"ibm", "img":"ibm.png", "score":100, "speed":5, "life":5},
    {"name":"lego", "img":"lego.png", "score":100, "speed":5, "life":5},
    {"name":"line", "img":"line.png", "score":100, "speed":5, "life":5},
    {"name":"mcdonalds", "img":"mcdonalds.png", "score":100, "speed":5, "life":5},
    {"name":"nasa", "img":"nasa.png", "score":100, "speed":5, "life":5},
    {"name":"nike", "img":"nike.png", "score":100, "speed":5, "life":5},
    {"name":"sony", "img":"sony.png", "score":100, "speed":5, "life":5},
    {"name":"starbucks", "img":"starbucks.png", "score":100, "speed":5, "life":5},
    {"name":"twitter", "img":"twitter.png", "score":100, "speed":5, "life":5},
)
SHOT_IMAGES = (
    "p_shot1.png",
    "p_shot2.png",
    "e_shot1.png",
    "e_shot2.png",
)
COLLAPSE_IMAGE = "explosion.png"
BACKGROUND_IMAGE = "background.png"

GAME_TITLE = "がんばれ弊社"
START_MESSAGE = "PRESS ENTER KEY"
GAMEOVER_MESSAGE = "GAME OVER"
PAUSE_MESSAGE = "PAUSE"

SCORE_TEXT = "SCORE"
HIGH_SCORE_TEXT = "HI-SCORE"

class Event(Enum):
    """ゲーム内で扱う入力イベントの種類です。"""
    ENTER = auto()
    ESCAPE = auto()
    QUIT = auto()

class GameState(Enum):
    """ゲーム画面の状態を表します。"""
    RUNNING = auto()
    STARTING = auto()
    PAUSE = auto()

def main():
    """ゲームを初期化し、メインループを実行します。"""
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_RECT.size)
    pygame.display.set_caption(GAME_TITLE)
    font = pygame.font.Font(None,60)
    font_lg = pygame.font.Font(None,80)
    font_sm = pygame.font.Font(None,30)

    game_state = GameState.STARTING
    game_count = 0
    high_score = 0
    current_score = 0
    _, score_height = font_sm.size(str(current_score))
    score_text = font_sm.render(f"{SCORE_TEXT}: {current_score}", True, (255,255,255))
    high_score_text = font_sm.render(f"{HIGH_SCORE_TEXT}: {high_score}", True, (255,255,255))

    # 画面中央に表示するメッセージを先に画像化しておきます。
    text_width, text_height = font.size(START_MESSAGE)
    text = font.render(START_MESSAGE, True, (255,255,255))
    text_width_gameover, text_height_gameover = font_lg.size(GAMEOVER_MESSAGE)
    text_gameover = font_lg.render(GAMEOVER_MESSAGE, True, (255,255,255))
    text_width_pause, text_height_pause = font.size(PAUSE_MESSAGE)
    text_pause = font.render(PAUSE_MESSAGE, True, (255,255,255))

    # スプライトグループを作成して登録
    all_sprite = pygame.sprite.RenderUpdates()
    enemies = pygame.sprite.Group()  # 敵グループ
    player_shots = pygame.sprite.Group()   # プレイヤの弾グループ
    enemy_shots = pygame.sprite.Group()   # 敵の弾グループ
    background = pygame.sprite.Group()   # 背景グループ
    Player.containers = all_sprite
    PlayerShot.containers = all_sprite, player_shots
    Enemy.containers = all_sprite, enemies
    EnemyShot.containers = all_sprite, enemy_shots

    # 画像の読込み
    shot_images = [load_image(IMAGE_DIR+img) for img in SHOT_IMAGES]

    # スプライトの画像を登録
    Background.image = load_image(IMAGE_DIR+BACKGROUND_IMAGE)
    PlayerShot.image = shot_images[1]
    EnemyShot.image = shot_images[2]

    bg_sprite1 = Background(0,-Background.image.get_size()[1])
    bg_sprite2 = Background(0,0)
    background.add(bg_sprite1)
    background.add(bg_sprite2)

    clock = pygame.time.Clock()

    while True:
        game_count += 1

        # ゲーム開始時、ゲームオーバー時の画面
        while game_state == GameState.STARTING:
            bg_sprite1.draw(screen)
            bg_sprite2.draw(screen)
            screen.blit(score_text,(0,0))
            screen.blit(high_score_text,(0,score_height))
            screen.blit(text,(int((WINDOW_WIDTH-text_width)/2),int((WINDOW_HEIGHT-text_height)/2)))
            if game_count > 1:
                screen.blit(text_gameover,(int((WINDOW_WIDTH-text_width_gameover)/2),int((WINDOW_HEIGHT-text_height_gameover)/3)))

            pygame.display.update()
            if command_input() == Event.ENTER:
                current_score = 0
                game_state = GameState.RUNNING
                # ENTER が押されたらプレイヤーと敵を作り直してゲーム開始です。
                player = Player(PLAYER_DATA)
                add_enemies(3,20)


        if game_state == GameState.RUNNING:
            # 敵を全部倒したらおかわり
            if len(enemies.sprites()) <= 0:
                add_enemies(3,20)

            # ゲームオーバー時
            if not player.alive():
                [sprite.kill() for sprite in enemies.sprites()]
                [sprite.kill() for sprite in enemy_shots.sprites()]
                [sprite.kill() for sprite in player_shots.sprites()]
                game_state = GameState.STARTING

            # 1 秒間に 60 回程度の更新になるようにします。
            clock.tick(60)
            all_sprite.update()

            # 衝突判定
            current_score += collision_detection(player, enemies, player_shots, enemy_shots)
            if current_score >= high_score:
                high_score = current_score
            _, score_height = font_sm.size(str(current_score))
            score_text = font_sm.render(f"{SCORE_TEXT}: {current_score}", True, (255,255,255))
            high_score_text = font_sm.render(f"{HIGH_SCORE_TEXT}: {high_score}", True, (255,255,255))

            # 背景、スプライト、スコアの順に描画します。
            background.update()
            bg_sprite1.draw(screen)
            bg_sprite2.draw(screen)
            all_sprite.draw(screen)
            screen.blit(score_text,(0,0))
            screen.blit(high_score_text,(0,score_height))
            pygame.display.update()

        elif game_state == GameState.PAUSE:
            bg_sprite1.draw(screen)
            bg_sprite2.draw(screen)
            all_sprite.draw(screen)

            screen.blit(score_text,(0,0))
            screen.blit(high_score_text,(0,score_height))
            screen.blit(text_pause, (int((WINDOW_WIDTH-text_width_pause)/2),int((WINDOW_HEIGHT-text_height_pause)/2)))
            pygame.display.update()

        if command_input() == Event.ESCAPE:
            if game_state == GameState.RUNNING:
                game_state = GameState.PAUSE
            elif game_state == GameState.PAUSE:
                game_state = GameState.RUNNING


def command_input(arg=None):
    """キーボードや終了ボタンの入力を確認し、ゲーム用イベントに変換します。"""
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            return Event.ESCAPE

            return Event.ESCAPE
        elif event.type == KEYDOWN and event.key in (K_RETURN,K_KP_ENTER):
            return Event.ENTER


def collision_detection(player, enemies, player_shots, enemy_shots):
    """弾や敵との衝突を判定し、加算するスコアを返します。"""
    # 敵と弾の衝突判定
    enemy_collided = pygame.sprite.groupcollide(enemies, player_shots, False, True)
    # enemy_collided.update(pygame.sprite.groupcollide(enemies, enemy_shots, False, True)) # 敵が敵の弾にも当たるようになる
    for enemy in list(enemy_collided.keys()):
        if not enemy.damaged:
            enemy.damage()
        if enemy.life == 0:
            return enemy.score
  
    # プレイヤーと弾の衝突判定
    beam_collided = pygame.sprite.spritecollide(player, enemy_shots, True)
    if beam_collided and not player.damaged:
        player.damage()

    # 弾同士の衝突判定
    shot_collided = pygame.sprite.groupcollide(enemy_shots, player_shots, True, True)

    return 0


def add_enemies(min, max):
    """min から max 未満のランダムな数だけ敵を追加します。"""
    for _ in range(0, np.random.randint(min, max)):
        Enemy((ENEMIES_DATA[np.random.randint(len(ENEMIES_DATA))]))


def load_image(filename, colorkey=None):
    """
    画像を読み込み、アルファチャンネル付きの Surface として返します。
    """
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert_alpha()
    return image


def set_alpha(surface, color, offset=(0,0), back=False):
    """
    Surface を指定色で塗った画像を重ねます。

    影やダメージ時の点滅画像を作るために使います。
    offset で位置をずらし、back=True で元画像の背面に配置します。
    """
    alpha = surface.copy()
    fill(alpha, color)

    image_rect = surface.get_rect()
    alpha_rect = alpha.get_rect()
    alpha_rect.center = image_rect.center
    alpha_rect.move_ip(offset)

    union_rect = image_rect.union(alpha_rect)
    new_surface = pygame.Surface(union_rect.size, pygame.SRCALPHA)

    args=[(surface,(0,0)),(alpha,offset)]
    if back: args.reverse()
    list(new_surface.blit(arg[0],arg[1]) for arg in args)

    return {"surface":new_surface, "rect":image_rect}


def fill(surface, color):
    """
    Surface の透明度を保ったまま、指定色で塗りつぶします。
    """
    w,h = surface.get_size()
    r,g,b,a = color
    for x in range(w):
        for y in range(h):
            new_alpha = surface.get_at((x,y))[3] and a
            surface.set_at((x,y), pygame.Color(r,g,b,new_alpha))


def make_logo(filename):
    """通常時とダメージ時に使うロゴ画像を作成します。"""
    image = load_image(filename)
    flicker_image = set_alpha(image.copy(),FLICKER_COLOR)["surface"]
    logo_images = []
    logo_images.append(set_alpha(image,SHADOW_COLOR,SHADOW_OFFSET,True))
    logo_images.append(set_alpha(flicker_image,SHADOW_COLOR,SHADOW_OFFSET,True))
    return logo_images


class Company(pygame.sprite.Sprite):
    """
    プレイヤーと敵に共通する情報と処理をまとめた親クラスです。
    """
    def __init__(self, data):
        super().__init__(self.containers)
        self.name = data["name"]
        self.logo = make_logo(IMAGE_DIR+data["img"])
        self.score = data["score"]
        self.life = data["life"]
        self.speed = data["speed"]
        self.image = self.logo[0]["surface"]
        self.rect = self.logo[0]["rect"]
        self.collapse_flame = 30
        self.damage_flame = 20
        self.damaged = False

    def damage(self):
        """ダメージを受けたときにライフを減らし、点滅状態にします。"""
        self.life -= 1
        self.damaged = True

    def collapse(self):
        """ライフが 0 になったときの爆発表示と消滅処理です。"""
        self.image = load_image(IMAGE_DIR+COLLAPSE_IMAGE)
        self.speed = 0
        self.collapse_flame -= 1
        if self.collapse_flame <= 0:
            self.kill()

    def update(self):
        """ダメージ時の点滅と、ライフがなくなったときの処理を行います。"""
        if self.damaged:
            self.damage_flame -= 1
            self.image = self.logo[self.damage_flame%2]["surface"]
            if self.damage_flame <= 0:
                self.image = self.logo[0]["surface"]
                self.damage_flame = 20
                self.damaged = False

        if self.life <= 0:
            self.collapse()

class Player(Company):
    """
    プレイヤーが操作する自機です。
    """
    def __init__(self, data):
        super().__init__(data)
        self.reload_time = 30  # リロード時間

        self.rect.bottom = SCREEN_RECT.bottom  # プレイヤーが画面の一番下
        self.reload_timer = 0

    def update(self):
        super().update()
        # 押されているキーをチェック
        pressed_keys = pygame.key.get_pressed()
        # 押されているキーに応じてプレイヤーを移動
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        elif pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        elif pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        elif pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        self.rect.clamp_ip(SCREEN_RECT)
        # 弾の発射
        if pressed_keys[K_SPACE]:
            # リロード時間が 0 になるまで再発射できない
            if self.reload_timer > 0:
                # リロード中
                self.reload_timer -= 1
            else:
                # 発射！！！
                PlayerShot(self.rect.midtop)  # 作成すると同時に all に追加される
                PlayerShot(self.rect.midtop,deg=10)  # 作成すると同時に all に追加される
                PlayerShot(self.rect.midtop,deg=-10)  # 作成すると同時に all に追加される
                self.reload_timer = self.reload_time

class Enemy(Company):
    """
    ランダムに移動し、一定確率で弾を撃つ敵です。
    """
    def __init__(self, data):
        super().__init__(data)
        # self.prob_beam = 0.0105  # 弾を発射する確率
        self.prob_beam = 0.01  # 弾を発射する確率
        self.forward_frame = np.random.randint(5,50)   # 出現してから直進するフレーム数
        self.rect.midtop = ((np.random.randint(80,SCREEN_RECT.width-80),0))

        self.wait_frame = 0 # 待機するフレーム数
        self.move_frame = 0 # 移動するフレーム数
        self.direction = 0 # 移動する方向

    def update(self):
        super().update()

        # 移動 または 待機 を決定する
        if self.wait_frame <= 0 and self.move_frame <= 0:
            if np.random.randint(0,10) >= 8:
                self.move_frame = np.random.randint(5,20)
                self.direction = np.radians(np.random.randint(0,365))
            else:
                self.wait_frame = np.random.randint(5,20)

        # 出現時
        if self.forward_frame > 0:
            self.forward_frame -= 1
            self.rect.move_ip(0,np.random.randint(6))

        else:
            # 移動
            if self.move_frame > 0:
                self.move_frame -= 1
                self.rect.move_ip(np.cos(self.direction)*self.speed, np.sin(self.direction)*self.speed)

            # 待機
            elif self.wait_frame > 0:
                self.wait_frame -= 1

            # 弾を発射
            if np.random.random() < self.prob_beam:
                EnemyShot(self.rect.midbottom)
                if np.random.randint(1,10) >= 6:
                    EnemyShot(self.rect.midbottom,deg=20)
                    EnemyShot(self.rect.midbottom,deg=-20)

        # 画面外に出ると消える
        if self.rect.top < 0 or self.rect.bottom > SCREEN_RECT.height or self.rect.right < 0 or self.rect.left > SCREEN_RECT.width:
            self.kill()


class Shot(pygame.sprite.Sprite):
    """
    プレイヤーと敵の弾に共通する処理をまとめた親クラスです。
    """
    def __init__(self, deg):
        # image と containers は main() でセット
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.rect = self.image.get_rect()
        self.speed = 0
        self.direction = 0
        self.deg = deg

    def update(self):
        # deg の値を変えると、斜め方向の弾になります。
        self.rect.move_ip(
            self.direction*self.speed*np.sin(np.radians(self.deg)),
            self.direction*self.speed*np.cos(np.radians(self.deg))
        )  # 上へ移動

        if self.rect.top < 0 or self.rect.bottom > SCREEN_RECT.height:  # 上端または下端に達したら除去
            self.kill()

class PlayerShot(Shot):
    """
    プレイヤーが撃つ弾です。
    """
    def __init__(self, pos, deg=0):
        super().__init__(deg)
        self.rect.midbottom = pos # Shot の出現位置
        self.speed = 6
        self.direction = -1

class EnemyShot(Shot):
    """
    敵が撃つ弾です。
    """
    def __init__(self, pos, deg=0):
        super().__init__(deg)
        self.rect.midtop = pos # Shot の出現位置
        self.speed = 5
        self.direction = 1

class Background(pygame.sprite.Sprite):
    """縦方向にスクロールする背景です。"""
    x = 0
    y = 0
    scroll_speed = 2
    def __init__(self, x=0,y=0):
        super(Background,self).__init__()
        self.x=x
        self.y=y
        
        self.rect = self.image.get_rect()

    def scroll(self,speed):
        self.y+=(speed)
        if self.y>self.image.get_size()[1]:
            self.y=-self.image.get_size()[1]

    def update(self):
        self.scroll(self.scroll_speed)
    
    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))


if __name__ == "__main__":
    main()
