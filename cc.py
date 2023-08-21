import httpx
import time
import sys
import os

url ='http://127.0.0.1:8000/upload'
files = {'file': open(sys.argv[1], 'rb')}
headers={'file': os.path.basename(sys.argv[1])}
timeout = httpx.Timeout(None, read=180.0)

with httpx.Client(timeout=timeout) as client:
    start = time.time()
    r = client.post(url, files=files, headers=headers)
    end = time.time()
    print(f'Time elapsed: {end - start}s')
    print(r.status_code, r.json(), sep=' ')
