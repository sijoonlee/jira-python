import concurrent.futures
import time

counter = 0


def increment_counter(fake_value):
    global counter
    time.sleep(1)
    for _ in range(100):
        counter += 1


if __name__ == "__main__":
    fake_data = [x for x in range(10)]
    counter = 0
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(increment_counter, fake_data)
    duration = time.time() - start_time
    print(duration)