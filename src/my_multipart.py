from concurrent.futures import ThreadPoolExecutor

from .sendfile import sendfile
from .constants import CHUNK_SIZE

class UploadFileByStream:
    def __init__(self):
        self.buffer = None
        self.bytes_received = None
        self.executor = ThreadPoolExecutor()
        self.urls = []
        self.futures = []

    def on_part_begin(self):
        self.buffer = b""
        self.bytes_received = 0

    def on_part_data(self, data, start, end):
        self.buffer += data[start:end]
        self.bytes_received += end - start

        if self.bytes_received >= CHUNK_SIZE:
            self.send_buffer()

    def on_part_end(self):
        if self.buffer:
            self.send_buffer()

    def send_buffer(self):
        future = self.executor.submit(sendfile, self.buffer)
        self.futures.append(future)

        self.buffer = b""
        self.bytes_received = 0

    def collect_urls(self):
        for future in self.futures:
            try:
                result = future.result()
                self.urls.extend(result)
            except Exception as e:
                print("Error while processing chunk:", e)
