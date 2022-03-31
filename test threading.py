from threading import Thread
import time

def delayed1():
    time.sleep(5)
    print("Вывод через 5 секунд!")
    

def delayed2():
    print("ВЫВОД")


th = Thread(target=delayed1)
th2 = Thread(target=delayed2)
th.start()
th2.start()


