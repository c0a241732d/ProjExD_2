import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
os.chdir(os.path.dirname(os.path.abspath(__file__)))
DELTA = {
            pg.K_UP: (0, -5),
            pg.K_DOWN: (0, 5),
            pg.K_LEFT: (-5, 0),
            pg.K_RIGHT: (5, 0)
        }


def cheak_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果, 縦方向判定結果）
    画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向はみだしチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向はみだしチェック
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    引数：元の画面
    戻り値：なし
    ゲームオーバーになったときにゲームオーバー画面に切り替える
    """
    # 
    bs_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(bs_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))  # 黒い四角を描写
    bs_img.set_alpha(100)  # 透明度設定
    # 文字
    go_img = pg.font.Font(None, 80)  # フォントサイズ
    go_txt = go_img.render("Game Over", True, (255, 255, 255))  # フォント色など
    bs_img.blit(go_txt, [450, 325])  # フォント位置
    # こうかとん
    gokk_img = pg.image.load("fig/8.png")
    bs_img.blit(gokk_img, [400, 300])  # こうかとん位置
    bs_img.blit(gokk_img, [760, 300])  # こうかとん位置

    screen.blit(bs_img, [0, 0])
    pg.display.update()
    time.sleep(5)  # 5秒表示


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    引数：なし
    戻り値：10段階の爆弾の大きさ、加速度のリスト
    時間とともに爆弾がでかくなり、速くなる
    """
    bb_imgs = []

    for r in range(1, 11):  # 爆弾の設定
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255, 0, 0), (10*r, 10*r), 10*r)  # 赤色の爆弾
        bb_img.set_colorkey((0, 0, 0))
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1, 11)]  # 爆弾の加速度
    return bb_imgs, bb_accs

# 演習3途中
# def get_kk_omgs() -> dict[tuple[int, int], pg.Surface]:
#     kk_img = pg.image.load("fig/3.png")

#     kk_dict = {
#         (0, 0): rotozoom(pg.transform.rotozoom())
#     }


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20, 20))
    pg.draw.circle(bb_img, (255, 0, 0), (10, 10), 10)  # 赤色で半径10の爆弾
    bb_img.set_colorkey((0, 0, 0))  # 黒色を透過
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)  # 爆弾の位置を乱数で決定
    clock = pg.time.Clock()
    tmr = 0
    vx = 5
    vy = 5
    bb_imgs, bb_accs = init_bb_imgs()  # init_bb_imgs関数を呼び出す
    
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return

        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            gameover(screen)  # gameover関数を引数screenで呼び出す
            return 
            
        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for k, mv in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += mv[0]  # 横方向の移動量 
                sum_mv[1] += mv[1]  # 縦方向の移動量

        kk_rct.move_ip(sum_mv)

        if cheak_bound(kk_rct) != (True, True):  # 関数cheak_boundを引数kk_rctで呼び出す
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko, tate = cheak_bound(bb_rct)  # 関数cheak_boundを引数bb_rctで呼び出す

        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        # 加速度
        avx = vx*bb_accs[min(tmr//500, 9)]
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_rct.move_ip(avx, avy)
        # width, heightの更新
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.width = bb_img.get_rect().width
        bb_rct.height = bb_img.get_rect().height
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
