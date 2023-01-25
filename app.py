import asyncio
import os
import requests
import shutil

FREQ = int(os.getenv("FREQ", 60))
API_KEY = os.getenv("API_KEY", "Kns9wdjHcCCZ5W9NkX7mNYMkjuuJzqYi")
IP_ADDRESS = os.getenv("IP_ADDRESS", "192.168.1.50")
PORT = os.getenv("PORT", "8384")
SYNC_DIR = "/mnt/sync"
COMPLETION_DIR = "/mnt/completion"

async def periodic():
    while True:       
        try: 
            syncTask()
        except Exception as e:
            print(f"Error when running syncTask: {e}")
        await asyncio.sleep(FREQ)

def syncTask():
    print("Syncing")
    url = f"http://{IP_ADDRESS}:{PORT}/rest/db/completion"    
    response = requests.get(url, headers={"X-API-KEY":API_KEY})
    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        return

    status = response.json()
    completion = status["completion"]
    if completion != 100:
        print(f"Sycning in progress: {completion}")
        return

    if not os.path.exists(SYNC_DIR):
        print(f"SYNC_DIR {SYNC_DIR} does not exist")
        return

    if not os.path.exists(COMPLETION_DIR):
        print(f"COMPLETION_DIR {COMPLETION_DIR} does not exist")
        return

    for entry in os.scandir(SYNC_DIR):
        if entry.is_dir and entry.name == ".stfolder":
            continue
        print(f"Moving {entry} to DST")
        shutil.move(entry.path, COMPLETION_DIR)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(periodic())

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass