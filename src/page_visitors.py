import datetime
import requests
import time
import random
from settings import config
from utils import load_from_json, save_to_json

headers = {
    "Content-Type": "application/json",
    "Cookie": f"{config.COOKIE}"
}

def extract_page_info():
    pages = load_from_json('pages.json')
    page_info = []
    for page in pages:
        if page['object'] == 'page':
            page_id = page['id']
            # Usando o método get para evitar KeyError
            title_property = page['properties'].get('title', {})
            title_list = title_property.get('title', [])
            page_title = title_list[0]['plain_text'] if title_list else 'Sem título'
            page_url = page.get('url', 'Sem URL')  # Obtendo a URL
            page_info.append((page_id, page_title, page_url))  # Incluindo a URL na tuple
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

def main():
    start_time = datetime.datetime.now()
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    page_info = extract_page_info()
    total_pages = len(page_info)
    print(f"Total pages: {total_pages}")
    visitors_data = {}
    for index, (page_id, page_title, page_url) in enumerate(page_info, start=1):
        print(f"{index}/{total_pages}: {page_id} - {page_title} - {page_url}")
        visitors = get_page_visitors(page_id)
        visitors_data[page_id] = visitors
        time.sleep(random.uniform(0.5, 2.0))

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}")

    save_to_json(visitors_data, 'visitors.json')

if __name__ == "__main__":
    main()
