import httpx
import json
import uuid
from constants import MASTODON_API_URL, BEARER_ACCESS_TOKEN, JSON_FILE_PATH

HEADERS = {
    "Authorization": f"Bearer {BEARER_ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Added By: Vatsal Gandhi
async def create_mastodon_post(content: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{MASTODON_API_URL}/statuses/",
            headers={**HEADERS, "Idempotency-Key": str(uuid.uuid4())},
            json={"status": content, "visibility": "public"},
        )
        if response.status_code == 200:
            post_data = response.json()
            post_id = str(post_data.get("id"))
            timestamp = post_data.get("created_at")
            if post_id:
                save_post_id(post_id)
            return post_data
        return None

# Added By: Vatsal Gandhi
async def get_mastodon_post(post_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{MASTODON_API_URL}/statuses/{post_id}",
            headers=HEADERS,
        )
        return response.json() if response.status_code == 200 else None

# Added By: Harishita Gupta
async def delete_mastodon_post(post_id: str):
    async with httpx.AsyncClient() as client:
        response = await client.delete(
            f"{MASTODON_API_URL}/statuses/{post_id}",
            headers=HEADERS,
        )
        if response.status_code == 200:
            remove_post_id(post_id)
        return response.status_code == 200

# Added By: Vatsal Gandhi
def save_post_id(post_id: str):
    try:
        with open(JSON_FILE_PATH, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[post_id] = True

    with open(JSON_FILE_PATH, "w") as file:
        json.dump(data, file, indent=4)

# Added By: Harishita Gupta
def get_all_post_ids():
    try:
        with open(JSON_FILE_PATH, "r") as file:
            data = json.load(file)
        return list(data.keys())
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Added By: Harishita Gupta
def remove_post_id(post_id: str):
    try:
        with open(JSON_FILE_PATH, "r") as file:
            data = json.load(file)
        
        if post_id in data:
            del data[post_id]
        
        with open(JSON_FILE_PATH, "w") as file:
            json.dump(data, file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
