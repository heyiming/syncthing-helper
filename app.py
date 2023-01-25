import asyncio, os, requests

FREQ = int(os.getenv("FREQ", 10))
API_KEY = os.getenv("API_KEY", "Kns9wdjHcCCZ5W9NkX7mNYMkjuuJzqYi")
IP_ADDRESS = os.getenv("IP_ADDRESS", "192.168.1.50")
PORT = os.getenv("PORT", "8384")

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

    
    


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(periodic())

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass