import threading
import time
import random

# =========================
# Shared memory
# =========================
buffer = [None] * 100
in_index = 0
out_index = 0

# =========================
# Semaphores and initial values
# =========================
emptyPairs = threading.Semaphore(50)   # 50 pair-slots free
fullPairs = threading.Semaphore(0)     # 0 ready pairs
mutex = threading.Semaphore(1)         # protect buffer, in_index, out_index

# =========================
# Control
# =========================
NUM_PRODUCERS = 3
stop_event = threading.Event()

print_lock = threading.Lock()
pair_id_lock = threading.Lock()
next_pair_id = 1

ERROR_CHANCE = 0.10   # 10% chance of machine error each loop


# =========================
# Helper functions
# =========================
def log(message):
    with print_lock:
        print(message)


def stop_system(message):
    log(message)
    stop_event.set()


def produce_pair(producer_id):
    global next_pair_id

    with pair_id_lock:
        pair_id = next_pair_id
        next_pair_id += 1

    P1 = f"Pair{pair_id}-P1-from-Producer{producer_id}"
    P2 = f"Pair{pair_id}-P2-from-Producer{producer_id}"
    return P1, P2, pair_id


def package_and_ship(P1, P2):
    log(f"Consumer packaged and shipped: {P1} and {P2}")


# =========================
# Producer
# =========================
def producer(producer_id):
    global in_index

    while True:
        if stop_event.is_set():
            log(f"Producer {producer_id} stopped.")
            break

        time.sleep(1)

        # machine error
        if random.random() < ERROR_CHANCE:
            stop_system(f"ERROR: Producer machine {producer_id} failed. Break loop.")
            break

        # Produce pair P1, P2
        P1, P2, pair_id = produce_pair(producer_id)

        # WAIT(emptyPairs) with timeout so thread can stop cleanly
        got_empty = emptyPairs.acquire(timeout=0.5)
        if not got_empty:
            continue

        if stop_event.is_set():
            emptyPairs.release()
            break

        # WAIT(mutex)
        got_mutex = mutex.acquire(timeout=0.5)
        if not got_mutex:
            emptyPairs.release()
            continue

        try:
            # Place P1 in buffer
            buffer[in_index] = P1

            # Place P2 in consecutive location
            second_pos = (in_index + 1) % 100
            buffer[second_pos] = P2

            log(
                f"Producer {producer_id} inserted Pair {pair_id} "
                f"at positions {in_index} and {second_pos}"
            )

            # move forward by 2
            in_index = (in_index + 2) % 100

        finally:
            # SIGNAL(mutex)
            mutex.release()

        # SIGNAL(fullPairs)
        fullPairs.release()


# =========================
# Consumer
# =========================
def consumer():
    global out_index

    while True:
        if stop_event.is_set():
            log("Consumer stopped.")
            break

        time.sleep(1)

        # machine error
        if random.random() < ERROR_CHANCE:
            stop_system("ERROR: Consumer machine failed. Break loop.")
            break

        # WAIT(fullPairs)
        got_full = fullPairs.acquire(timeout=0.5)
        if not got_full:
            continue

        if stop_event.is_set():
            fullPairs.release()
            break

        # WAIT(mutex)
        got_mutex = mutex.acquire(timeout=0.5)
        if not got_mutex:
            fullPairs.release()
            continue

        try:
            # Fetch P1 from buffer
            P1 = buffer[out_index]

            # Fetch P2 from buffer
            second_pos = (out_index + 1) % 100
            P2 = buffer[second_pos]

            # Clear slots
            buffer[out_index] = None
            buffer[second_pos] = None

            log(
                f"Consumer fetched from positions {out_index} and {second_pos}"
            )

            # move forward by 2
            out_index = (out_index + 2) % 100

        finally:
            # SIGNAL(mutex)
            mutex.release()

        # SIGNAL(emptyPairs)
        emptyPairs.release()

        # Package and ship
        if P1 is not None and P2 is not None:
            package_and_ship(P1, P2)


# =========================
# Main
# =========================
def main():
    random.seed()

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

    # Let program run until a machine error happens
    while not stop_event.is_set():
        time.sleep(0.5)

    # wait a little for threads to exit
    for t in threads:
        t.join(timeout=2)

    print("\nProgram ended.")


if __name__ == "__main__":
    main()