from concurrent.futures import ThreadPoolExecutor
import asyncio

from .sendfile import sendfile
from .constants import CHUNK_SIZE
from .crypto import encrypt
import time

class UploadFileByStream:
    def __init__(self):
        self.buffer = None
        self.bytes_received = None
        self.total_bytes = None
        self.executor = ThreadPoolExecutor()
        self.urls = []
        self.futures = []
        self.filename = None
        self.mimetype = None
        self.start = time.time()

    def on_part_begin(self):
        self.buffer = b""
        self.bytes_received = 0
        self.total_bytes = 0
        self.last_header_field = ""
        self.mimetype = ""

    def on_part_data(self, data, start, end):
        self.buffer += data[start:end]
        self.bytes_received += end - start
        self.total_bytes += end - start

        if self.bytes_received >= CHUNK_SIZE:
            self.send_buffer()

    def on_part_end(self):
        if self.buffer:
            self.send_buffer()

    def on_header_value(self, data, start, end):
        if self.last_header_field == "Content-Disposition" and b"filename=" in data[start:end]:
            self.filename = data[start:end].decode("utf-8").split("filename=")[1].strip('"')
        if self.last_header_field == "Content-Type":
            self.mimetype = data[start:end].decode("utf-8")

    def on_header_field(self, data, start, end):
        self.last_header_field = data[start:end].decode("utf-8")

    def send_buffer(self):
        future = self.executor.submit(sendfile, encrypt(self.buffer))
        self.futures.append(future)

        self.buffer = b""
        self.bytes_received = 0

    async def collect_urls(self):
        loop = asyncio.get_event_loop()
        futures = self.futures.copy()
        self.futures = []

        for future in futures:
            try:
                result = await loop.run_in_executor(None, future.result)
                self.urls.extend(result)
            except Exception as e:
                print("Error while processing chunk:", e)
