import threading
import time

class MyThread(threading.Thread):
    def __init__(self, name, delay):
        super().__init__()
        self.name = name
        self.delay = delay

    def run(self):
        for i in range(3):
            print(f"{self.name} running iteration {i+1}")
            time.sleep(self.delay)

if __name__ == "__main__":
    t1 = MyThread("Thread-A", 1)
    t2 = MyThread("Thread-B", 2)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("All class-based threads finished!")