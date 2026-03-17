import threading
import time

# Semaphores and initial values
a = threading.Semaphore(1)
b = threading.Semaphore(0)
c = threading.Semaphore(0)


# Process 1
def process1():
    while True:
        a.acquire()   # wait(a)

        print("H", end="")
        print("E", end="")

        b.release()   # signal(b)
        b.release()   # signal(b)


# Process 2
def process2():
    while True:
        b.acquire()   # wait(b)
        print("L", end="")

        b.acquire()   # wait(b)
        print("L", end="")

        c.release()   # signal(c)
        c.release()   # signal(c)


# Process 3
def process3():
    while True:
        c.acquire()   # wait(c)
        print("O", end="")

        c.acquire()   # wait(c)
        print("O")

        time.sleep(1)  # optional: makes output easier to read
        a.release()    # signal(a) to start next HELLOO


def main():
    t1 = threading.Thread(target=process1)
    t2 = threading.Thread(target=process2)
    t3 = threading.Thread(target=process3)

    t3.start()
    t2.start()
    t1.start()

    t1.join()
    t2.join()
    t3.join()


if __name__ == "__main__":
    main()