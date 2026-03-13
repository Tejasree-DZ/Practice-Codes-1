import threading
import time

def worker(name, delay):
    for i in range(3):
        print(f"{name} running iteration {i+1}")
        time.sleep(delay)

if __name__ == "__main__":
    t1 = threading.Thread(target=worker, args=("Function-Thread-A", 1))
    t2 = threading.Thread(target=worker, args=("Function-Thread-B", 2))

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print("All function-based threads finished!")