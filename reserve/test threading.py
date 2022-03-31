from threading import Thread
import threading
import time

def delayed1():
    time.sleep(5)
    print("Вывод через 10 секунд!")
    
th = Thread(target=delayed1)
th.start()

while True:
    for thread in threading.enumerate():
        time.sleep(1)
        print("Имя потока %s." % thread.getName())
