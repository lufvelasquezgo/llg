import time
from contextlib import contextmanager


@contextmanager
def timer(label: str):
    start = time.time()
    yield
    end = time.time()
    print(f"Task '{label}': {end - start:.3f}s")
