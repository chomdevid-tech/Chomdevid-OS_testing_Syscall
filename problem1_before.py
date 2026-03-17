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
fullPairs = threading.Semaphore(0)     # 0 full pairs ready
mutex = threading.Semaphore(1)         # protect buffer/in_index/out_index

# =========================
# Control variables
# =========================
NUM_PRODUCERS = 3
stop_event = threading.Event()

print_lock = threading.Lock()
pair_id_lock = threading.Lock()
next_pair_id = 1

# chance of machine error each loop
ERROR_CHANCE = 0.08


# =========================
# Helper functions
# =========================
def log(msg):
    with print_lock:
        print(msg)


def stop_system(message):
    log(message)
    stop_event.set()

    # release semaphores a few times so blocked threads can wake up and exit
    for _ in range(10):
        try:
            emptyPairs.release()
        except:
            pass
        try:
            fullPairs.release()
        except:
            pass
        try:
            mutex.release()
        except:
            pass


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
    time.sleep(0.5)


# =========================
# Producer
# =========================
def producer(producer_id):
    global in_index

    while True:
        if stop_event.is_set():
            log(f"Producer {producer_id} stopped.")
            break

        # simulate machine work
        time.sleep(0.5)

        # simulate machine error
        if random.random() < ERROR_CHANCE:
            stop_system(f"ERROR: Producer machine {producer_id} failed. Breaking loop.")
            break

        # Produce pair P1, P2
        P1, P2, pair_id = produce_pair(producer_id)

        # WAIT(emptyPairs)
        got_empty = emptyPairs.acquire(timeout=0.5)
        if not got_empty:
            continue

        if stop_event.is_set():
            log(f"Producer {producer_id} stopped.")
            break

        # WAIT(mutex)
        got_mutex = mutex.acquire(timeout=0.5)
        if not got_mutex:
            continue

        try:
            if stop_event.is_set():
                log(f"Producer {producer_id} stopped.")
                break

            # Place P1 in buffer
            buffer[in_index] = P1

            # Place P2 in buffer
            buffer[(in_index + 1) % 100] = P2

            log(
                f"Producer {producer_id} inserted Pair {pair_id} "
                f"at positions {in_index} and {(in_index + 1) % 100}"
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

        # simulate consumer machine work
        time.sleep(0.5)

        # simulate machine error
        if random.random() < ERROR_CHANCE:
            stop_system("ERROR: Consumer machine failed. Breaking loop.")
            break

        # WAIT(fullPairs)
        got_full = fullPairs.acquire(timeout=0.5)
        if not got_full:
            continue

        if stop_event.is_set():
            log("Consumer stopped.")
            break

        # WAIT(mutex)
        got_mutex = mutex.acquire(timeout=0.5)
        if not got_mutex:
            continue

        try:
            if stop_event.is_set():
                log("Consumer stopped.")
                break

            # Fetch P1 from buffer
            P1 = buffer[out_index]

            # Fetch P2 from buffer
            P2 = buffer[(out_index + 1) % 100]

            # Clear slots after taking
            buffer[out_index] = None
            buffer[(out_index + 1) % 100] = None

            log(
                f"Consumer fetched from positions {out_index} "
                f"and {(out_index + 1) % 100}"
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
    random.seed()  # random machine errors

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

    # Wait for all threads to finish
    for t in threads:
        t.join()

    print("\nProgram ended.")


if __name__ == "__main__":
    main()