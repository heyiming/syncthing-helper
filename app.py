#!/usr/bin/env python

import asyncio
import os
import requests
import shutil
import logging

# logging setup
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

FREQ = int(os.getenv("FREQ", 60))
API_KEY = os.getenv("API_KEY")
IP_ADDRESS = os.getenv("IP_ADDRESS", "192.168.1.50")
PORT = os.getenv("PORT", "8384")
SYNC_DIR = "/mnt/sync"
COMPLETION_DIR = "/mnt/completion"

async def periodic():
    while True:       
        try: 
            syncTask()
        except Exception as e:
            logger.error(f"Error when running syncTask: {e}")            
        await asyncio.sleep(FREQ)

def syncTask():
    logger.info("Checking")
    url = f"http://{IP_ADDRESS}:{PORT}/rest/db/completion"
    if not API_KEY:
        logger.error(f"API_KEY is unset")
        return        
    response = requests.get(url, headers={"X-API-KEY":API_KEY})
    if response.status_code != 200:
        logger.error(f"Request failed with status code {response.status_code}")        
        return

    status = response.json()
    completion = status["completion"]
    if completion != 100:
        logger.info(f"Sycning in progress: {completion} %")
        return

    if not os.path.exists(SYNC_DIR):
        logger.info(f"SYNC_DIR {SYNC_DIR} does not exist")
        return

    if not os.path.exists(COMPLETION_DIR):
        logger.info(f"COMPLETION_DIR {COMPLETION_DIR} does not exist")
        return

    for entry in os.scandir(SYNC_DIR):
        if entry.is_dir and entry.name == ".stfolder":
            continue
        logger.info(f"Moving {entry} to DST")
        shutil.move(entry.path, COMPLETION_DIR)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    task = loop.create_task(periodic())

    try:
        loop.run_until_complete(task)
    except asyncio.CancelledError:
        pass