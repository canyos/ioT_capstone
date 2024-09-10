from multiprocessing import Process
import multiprocessing
import time 
def control() :
    while True:
        print("sex")
        time.sleep(1)

if __name__ == '__main__':
    p0 = Process(target = control)
    p1 = Process(target = control)
    p2 = Process(target = control)
    p3 = Process(target = control)
    p4 = Process(target = control)
    p5 = Process(target = control)
    p6 = Process(target = control)
    p7 = Process(target = control)
    p0.start()
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p5.start()
    p6.start()
    p7.start()
    
    p0.join()
    p1.join()
    p2.join()
    p3.join()
    p7.join()
    p4.join()
    p5.join()
    p6.join()