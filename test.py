import threading
import time

result = None
done_event = threading.Event()
first = True

def get_action_thread():
    global result
    time.sleep(10)
    result = 10
    done_event.set()

def get_action():
    global first
    if first:
        thread = threading.Thread(target=get_action_thread)
        thread.start()
        first = False
        return None
    elif done_event.is_set():
        first = True
        done_event.clear()
        return result
    else:
        return None

# 示例使用
while True:
    action = get_action()
    if action is not None:
        print(action)
    print("waiting...")
    time.sleep(0.1)