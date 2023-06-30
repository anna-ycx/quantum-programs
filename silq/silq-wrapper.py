import time
import timeout_decorator
import os

@timeout_decorator.timeout(7200)
def run():
    start = time.time()
    os.system("./silq qft.slq --run")
    end = time.time()
    print(f"took {end - start}s")

run()