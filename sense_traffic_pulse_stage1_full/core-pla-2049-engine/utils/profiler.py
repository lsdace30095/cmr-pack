import time

class Profiler:
    """Simple execution time profiler."""

    def __init__(self):
        self.start = None

    def begin(self):
        self.start = time.time()

    def end(self):
        return time.time() - self.start
