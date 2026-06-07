#KHÔNG BUÔNG

# file âm thanh mọi người lưu clip về chuyển sang mp3 giúp mình nhé!
# Phát nhạc khi chạy hãy đặt tên file âm thanh là "music.mp3" rồi đặt file đó cùng thư mục
# bắt buộc cài pygame thì mới có âm thanh nhé

import time
import sys
import os

try:
    import pygame
    import threading
    pygame_ok = True
except ImportError:
    pygame_ok = False

if pygame_ok:
    pygame.mixer.init()

os.system("cls")

lyric = [
    "Anh cố để chi vậy? Rồi cũng ra như này",
    "Cứ vun mối tình, mặc tấm thân hao gầy",
    "Liệu có phút giây nào người xót anh không vậy?",
    "Mọi thứ chỉ để anh gánh lấy...",
    "",
    "Chẳng phút giây nào anh hết yêu em",
    "Mỗi lần ướt mi hoen là do anh nhớ em thêm",
    "Tại sao lại nói yêu anh mà lại để mi anh ướt nhèm???",
    "",
    "Em cũng có nỗi niềm của riêng mình",
    "Em xin lỗi đã bỏ anh một mình",
    "Sau bao tháng năm ta cùng chung đường",
    "Giờ hai đứa hai nơi...",
    "",
    "Đoạn cảm xúc tưởng như là lâu dài",
    "Nhưng lại kết thúc bất ngờ vì hiểu lầm",
    "Em trách sao lúc đó mình không vì nhau mà cố...",
    "",
    "Em vẫn còn nhớ những lần mình đã hứa hẹn",
    "Cùng nhau mãi mãi chẳng rời xa",
    "Và môi hôn vẫn để lại đó bao ngọt ngào xưa...",
    "",
    "Giờ thì đã quá trễ rồi vì phút bốc đồng",
    "Mà đôi ta chẳng thể nào cạnh bên",
    "Hỏi: 'Em còn yêu không?', em trả lời là: 'Không còn'",
    "Nhưng đó chỉ là dối lòng..."
]

thoi_gian_xuat_hien = [
    0, 4, 7, 10, 12, 14, 17, 21, 25.5, 28.5,
    32, 36, 39, 42, 43, 46, 49, 53, 56, 59,
    62, 65, 69, 72, 76, 79
]

toc_do_go_chu = [
    0.05, 0.05, 0.05, 0.05, 0.02, 0.05, 0.06, 0.07, 0.02, 0.07,
    0.07, 0.04, 0.04, 0.02, 0.05, 0.05, 0.05, 0.02, 0.05, 0.05,
    0.06, 0.02, 0.05, 0.05, 0.05, 0.08
]

def play_nhac_nen():
    if not pygame_ok:
        return
    
    danh_sach_nhac = ["background_music.mp3", "background_music.wav", "music.mp3", "music.wav"]
    file_nhac = None
    
    for file in danh_sach_nhac:
        if os.path.exists(file):
            file_nhac = file
            break
    
    if file_nhac:
        try:
            pygame.mixer.music.load(file_nhac)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play()
            threading.Timer(90, pygame.mixer.music.stop).start()
        except Exception:
            pass

def go_chu_do_ruc(line, delay=0.03, co_nen=False):
    for i, ch in enumerate(line):
        base_red = 180
        glow = int(75 * (i / max(len(line), 1)))
        r = min(255, base_red + glow)
        g = int(20 + glow * 0.3)
        b = int(10 + glow * 0.2)
        color = f"\033[38;2;{r};{g};{b}m"
        if co_nen:
            bg_color = "\033[48;2;30;0;0m"
            sys.stdout.write(bg_color + color + ch + "\033[0m")
        else:
            sys.stdout.write(color + ch + "\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def go_chu_nhip_tim(line, delay=0.025, co_nen=False):
    for i, ch in enumerate(line):
        pulse = int(55 * abs((i * 0.3) % 2 - 1))
        r = 200 + pulse
        g = int(30 + pulse * 0.4)
        b = int(20 + pulse * 0.3)
        color = f"\033[38;2;{r};{g};{b}m"
        if co_nen:
            bg_color = "\033[48;2;25;0;5m"
            sys.stdout.write(bg_color + color + ch + "\033[0m")
        else:
            sys.stdout.write(color + ch + "\033[0m")
        sys.stdout.flush()
        time.sleep(delay * (0.8 + 0.4 * (i % 2)))
    print()

def go_chu_lua(line, delay=0.028, co_nen=False):
    for i, ch in enumerate(line):
        flicker = int(30 * ((i * 7) % 3))
        r = 255 - flicker
        g = int(60 + (i * 9) % 95 + flicker * 0.5)
        b = int(10 + (i * 3) % 30)
        color = f"\033[38;2;{r};{g};{b}m"
        if co_nen:
            bg_color = "\033[48;2;40;5;0m"
            sys.stdout.write(bg_color + color + ch + "\033[0m")
        else:
            sys.stdout.write(color + ch + "\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def go_chu_nhung_do(line, delay=0.035, co_nen=False):
    for i, ch in enumerate(line):
        depth = int(80 * (1 - i / max(len(line), 1)))
        r = 160 + depth
        g = int(25 + depth * 0.2)
        b = int(35 + depth * 0.1)
        color = f"\033[38;2;{r};{g};{b}m"
        if co_nen:
            bg_color = "\033[48;2;20;0;10m"
            sys.stdout.write(bg_color + color + ch + "\033[0m")
        else:
            sys.stdout.write(color + ch + "\033[0m")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def go_chu_song_do(line, delay=0.022, co_nen=False):
    n = len(line)
    for i in range(n):
        wave_pos = i
        wave_width = 5
        visible = ""
        for j in range(n):
            distance = abs(j - wave_pos)
            if distance <= wave_width:
                intensity = 255 - (distance * 30)
                r = max(150, intensity)
                g = int(30 + (255 - intensity) * 0.3)
                b = int(20 + (255 - intensity) * 0.2)
            else:
                r,g,b = (80 + (j * 2) % 40),15,10
            color = f"\033[38;2;{r};{g};{b}m"
            if co_nen:
                bg_color = "\033[48;2;25;0;0m"
                visible += bg_color + color + line[j] + "\033[0m"
            else:
                visible += color + line[j] + "\033[0m"
        sys.stdout.write(f"\r{visible}")
        sys.stdout.flush()
        time.sleep(delay)
    
    final_line = ""
    for ch in line:
        r = 220 + (ord(ch) % 35)
        g = int(40 + (ord(ch) % 25))
        b = int(30 + (ord(ch) % 20))
        color = f"\033[38;2;{r};{g};{b}m"
        if co_nen:
            bg_color = "\033[48;2;25;0;0m"
            final_line += bg_color + color + ch + "\033[0m"
        else:
            final_line += color + ch + "\033[0m"
    sys.stdout.write(f"\r{final_line}\n")

def go_chu_than_hong(line, delay=0.032, co_nen=False):
    for i, ch in enumerate(line):
        base_r = 180
        pulse = int(45 * ((i * 0.4) % 2))
        r = base_r + pulse
        g = int(25 + pulse * 0.6)
        b = int(35 + pulse * 0.4)
        color = f"\033[38;2;{r};{g};{b}m"
        if co_nen:
            bg_color = "\033[48;2;35;0;5m"
            sys.stdout.write(bg_color + color + ch + "\033[0m")
        else:
            sys.stdout.write(color + ch + "\033[0m")
        sys.stdout.flush()
        time.sleep(delay * (0.9 + 0.2 * (i % 3)))
    print()

def dong_trong():
    print()
    time.sleep(0.5)

hieu_ung = [
    go_chu_do_ruc,
    go_chu_nhip_tim,
    go_chu_lua,
    go_chu_nhung_do,
    go_chu_song_do,
    go_chu_than_hong
]

os.system("cls")

thoi_gian_bat_dau = time.time()

if pygame_ok:
    music_thread = threading.Thread(target=play_nhac_nen)
    music_thread.daemon = True
    music_thread.start()

so_dong = 0

for i, line in enumerate(lyric):
    thoi_gian_muc_tieu = thoi_gian_xuat_hien[i]
    thoi_gian_troi_qua = time.time() - thoi_gian_bat_dau
    if thoi_gian_troi_qua < thoi_gian_muc_tieu:
        time.sleep(thoi_gian_muc_tieu - thoi_gian_troi_qua)
    if line == "":
        dong_trong()
        continue
    co_nen = (so_dong % 2 == 1)
    
    if so_dong < 4:
        index_hieu_ung = so_dong % 3
    elif so_dong >= 4 and so_dong < 8:
        index_hieu_ung = 3 + (so_dong % 2)
    elif so_dong >= 8 and so_dong < 12:
        index_hieu_ung = 2 + (so_dong % 3)
    elif so_dong >= 12:
        index_hieu_ung = 4 + (so_dong % 2)
    else:
        index_hieu_ung = so_dong % len(hieu_ung)
    
    effect = hieu_ung[index_hieu_ung]
    speed = toc_do_go_chu[i] if i < len(toc_do_go_chu) else 0.035
    effect(line, speed, co_nen)   
    so_dong += 1

tong_thoi_gian = time.time() - thoi_gian_bat_dau
if tong_thoi_gian < 90:
    time.sleep(90 - tong_thoi_gian)

time.sleep(2)
