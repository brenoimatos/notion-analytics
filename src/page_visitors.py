import requests
import json
import os
import time
import random
from settings import config

headers = {
    "Content-Type": "application/json",
    "Cookie": f"{config.COOKIE}"
}

def extract_page_info():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', 'pages.json')
    with open(file_path, 'r') as f:
        pages = json.load(f)
    page_info = []
    for page in pages:
        if page['object'] == 'page':
            page_id = page['id']
            # Usando o método get para evitar KeyError
            title_property = page['properties'].get('title', {})
            title_list = title_property.get('title', [])
            page_title = title_list[0]['plain_text'] if title_list else 'Sem título'
            page_info.append((page_id, page_title))
    return page_info



def get_page_visitors(page_id):
    url = "https://www.notion.so/api/v3/getPageVisitors"
    data = {
        "block": {
            "id": page_id,
            "spaceId": "925b7f61-5287-4683-bf60-db4f84566eba"
        },
        "limit": 100
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def save_to_json(data):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, 'data')
    file_path = os.path.join(data_dir, 'visitors.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def main():
    page_info = extract_page_info()
    total_pages = len(page_info)
    print(f"Total pages: {total_pages}")
    visitors_data = {}
    for index, (page_id, page_title) in enumerate(page_info, start=1):
        print(f"{index}/{total_pages}: {page_id} - {page_title}")
        visitors = get_page_visitors(page_id)
        visitors_data[page_id] = visitors
        time.sleep(random.uniform(0.5, 2.0))
    save_to_json(visitors_data)

if __name__ == "__main__":
    main()
