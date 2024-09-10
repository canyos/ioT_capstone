import threading
import time
degree_1 = 0
flag_1 = 0
def handler():
    while True:
        global degree_1
        print (degree_1)
        if flag_1 == 0:
            degree_1 = degree_1 + 1
        time.sleep(1)


t = threading.Thread(target=handler)
t.start()

while True:
    for i in range (5):
        print("processing....")
        time.sleep(0.5)
    flag_1 = 1
    print("stopped")
