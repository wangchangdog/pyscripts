import pyautogui
import time
import random

interval = 60 * 4  # 4分ごとに動かす
last_position = None
idle_time = 0

while True:
    # 現在のマウスの位置を取得
    x, y = pyautogui.position()
    
    # 前回の位置と比較
    if last_position == (x, y):
        idle_time += 1
    else:
        idle_time = 0

    last_position = (x, y)

    # マウスが4分間動かなかった場合、マウスを動かす
    if idle_time > interval:
        # ランダム数値を生成
        rand_int_y = random.randint(-1, 1)
        rand_int_x = random.randint(-1, 1)
        # マウスを1px右に動かす
        pyautogui.moveTo(x + 1, y + 1)
        idle_time = 0

    # 次の動作まで待機
    time.sleep(1)