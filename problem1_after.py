import threading
import time

# Shared memory
buffer = [None] * 100
in_index = 0
out_index = 0

# Semaphores and initial values
emptyPairs = threading.Semaphore(50)   # 50 pair-slots
fullPairs = threading.Semaphore(0)     # 0 ready pairs
mutex = threading.Semaphore(1)         # protect shared memory

# Settings
NUM_PRODUCERS = 3

# For printing
print_lock = threading.Lock()

# Pair number
pair_id = 1
pair_id_lock = threading.Lock()


def log(message):
    with print_lock:
        print(message)


def produce_pair(producer_id):
    global pair_id

    with pair_id_lock:
        current_id = pair_id
        pair_id += 1

    P1 = f"Pair{current_id}-P1-from-Producer{producer_id}"
    P2 = f"Pair{current_id}-P2-from-Producer{producer_id}"
    return P1, P2, current_id


def package_and_ship(P1, P2):
    log(f"Consumer packaged and shipped: {P1} and {P2}")


def producer(producer_id):
    global in_index

    while True:
        time.sleep(1)

        # Produce pair P1, P2
        P1, P2, current_id = produce_pair(producer_id)

        # WAIT(emptyPairs)
        emptyPairs.acquire()

        # WAIT(mutex)
        mutex.acquire()

        # Place P1 in buffer
        buffer[in_index] = P1

        # Place P2 in consecutive position
        second_pos = (in_index + 1) % 100
        buffer[second_pos] = P2

        log(
            f"Producer {producer_id} inserted Pair {current_id} "
            f"at positions {in_index} and {second_pos}"
        )

        # Move forward by 2
        in_index = (in_index + 2) % 100

        # SIGNAL(mutex)
        mutex.release()

        # SIGNAL(fullPairs)
        fullPairs.release()


def consumer():
    global out_index

    while True:
        time.sleep(1)

        # WAIT(fullPairs)
        fullPairs.acquire()

        # WAIT(mutex)
        mutex.acquire()

        # Fetch P1 from buffer
        P1 = buffer[out_index]

        # Fetch P2 from buffer
        second_pos = (out_index + 1) % 100
        P2 = buffer[second_pos]

        # Clear slots
        buffer[out_index] = None
        buffer[second_pos] = None

        log(f"Consumer fetched from positions {out_index} and {second_pos}")

        # Move forward by 2
        out_index = (out_index + 2) % 100

        # SIGNAL(mutex)
        mutex.release()

        # SIGNAL(emptyPairs)
        emptyPairs.release()

        # Package and ship
        package_and_ship(P1, P2)


def main():
    threads = []

    # Start consumer
    c = threading.Thread(target=consumer)
    c.start()
    threads.append(c)

    # Start producers
    for i in range(1, NUM_PRODUCERS + 1):
        t = threading.Thread(target=producer, args=(i,))
        t.start()
        threads.append(t)

    # Keep program running
    for t in threads:
        t.join()


if __name__ == "__main__":
    main()