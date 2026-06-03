
import time
import sys
import os
from datetime import datetime
from typing import Optional, Tuple
import requests
try:
    from colorama import init as colorama_init
    colorama_init(autoreset=True)
except Exception:
    pass

den   = "\033[1;90m"
luc   = "\033[1;32m"
trang = "\033[1;37m"
do    = "\033[1;31m"
vang  = "\033[1;33m"
tim   = "\033[1;35m"
lamd  = "\033[1;34m"
lam   = "\033[1;36m"
hong  = "\033[1;95m"
reset = "\033[0m"

thanh_dep = trang + "~" + do + "[" + luc + "VNDEVCODE.COM" + do + "] " + trang + "➩ " + luc
API_URL = "https://keyherlyswar.x10.mx/Apidocs/reg/reglq.php"
TIMEOUT = 15
DELAY_BETWEEN = 5
MAX_RETRIES = 3
OUTPUT_FILE = "acclienquan.txt"  # lưu vào file txt cố định


def ask_positive_int(prompt: str) -> int:
    while True:
        raw = input(luc + prompt + vang).strip()
        print(reset, end="")
        try:
            n = int(raw)
            if n <= 0:
                print(do + "Vui lòng nhập một số nguyên dương." + reset)
                continue
            return n
        except ValueError:
            print(do + "Không hợp lệ. Hãy nhập số." + reset)


def create_garena_account(session: requests.Session) -> Tuple[bool, Optional[str], Optional[str], str]:
    try:
        res = session.get(API_URL, timeout=TIMEOUT)
    except requests.RequestException as e:
        return False, None, None, f"Lỗi mạng: {e}"

    if res.status_code != 200:
        return False, None, None, f"HTTP {res.status_code}"

    try:
        data = res.json()
    except Exception:
        return False, None, None, "Phản hồi không phải JSON"

    status = data.get("status")
    result = data.get("result")

    if not status or not result or not isinstance(result, list) or not result:
        return False, None, None, f"API trả về không hợp lệ"

    info = result[0] if isinstance(result[0], dict) else {}
    username = info.get("account") or info.get("username") or ""
    password = info.get("password") or ""

    if not username or not password:
        return False, None, None, f"Thiếu username/password"

    return True, username, password, "OK"


def countdown(seconds: int):
    for s in range(seconds, 0, -1):
        print(f"{den}  {s:2d}s...   {reset}", end="\r", flush=True)
        time.sleep(1)
    print(" " * 20, end="\r")


def main():
    os.system("cls" if os.name == "nt" else "clear")
    print(f"{thanh_dep}{trang}TOOL SCAN ACC LIÊN QUÂN VIP {den}\n")

    qty = ask_positive_int("Nhập số lượng acc scan: ")

    created = 0
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (compatible; RegGarenaBot/1.0)"})

    try:
        for i in range(1, qty + 1):
            print(f"\n{thanh_dep}{lam}Bắt đầu scan tài khoản {trang}[{vang}{i}{trang}/{vang}{qty}{trang}]{reset}")
            ok = False
            username = password = None

            for attempt in range(1, MAX_RETRIES + 1):
                print(f"{den}  → Thử lần {attempt}/{MAX_RETRIES}...{reset}")
                ok, username, password, _ = create_garena_account(session)
                if ok:
                    break
                else:
                    print(f"{do}  ✗ Thất bại, thử lại...{reset}")
                    if attempt < MAX_RETRIES:
                        time.sleep(2 * attempt)

            if ok and username and password:
                created += 1
                print(f"{luc}  ✓ Scan thành công!{reset}")
                print(f"{trang}     👤 Username: {hong}{username}{reset}")
                print(f"{trang}     🔑 Password: {hong}{password}{reset}")

                with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                    f.write(f"{username} | {password}\n")
            else:
                print(f"{do}  ❌ Không thể scan tài khoản.{reset}")

            if i < qty:
                print(f"{vang}⏳ Đợi {DELAY_BETWEEN} giây trước khi scan acc tiếp theo...{reset}")
                countdown(DELAY_BETWEEN)

    except KeyboardInterrupt:
        print(f"\n{do}⛔ Đã dừng theo yêu cầu (Ctrl+C).{reset}")

    print(f"\n{thanh_dep}{trang}Hoàn tất. Scan thành công: {luc}{created}{trang}/{vang}{qty}{reset}")
    print(f"{thanh_dep}{trang}Danh sách đã lưu tại: {lam}{OUTPUT_FILE}{reset}")


if __name__ == "__main__":
    main()


