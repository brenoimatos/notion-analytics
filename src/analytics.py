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

def extract_page_info(filter_pages_with_title):
    pages = load_from_json('parsed/parsed_pages.json')
    page_info = []
    for page in pages:
        page_id = page['id']
        page_title = page.get('page_title', None)
        alternative_title = page.get('alternative_title', 'Sem título')
        page_url = page.get('url', 'Sem URL')
        
        if filter_pages_with_title and page_title is None:
            continue

        display_title = page_title if page_title is not None else alternative_title
        page_info.append((page_id, display_title, page_url))
    return page_info

def get_page_analytics(page_id):
    url = "https://www.notion.so/api/v3/getPageAnalytics"
    data = {
        "pageId": page_id,
        "spaceId": "925b7f61-5287-4683-bf60-db4f84566eba"
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

def main(filter_pages_with_title):
    start_time = datetime.datetime.now()
    print(f"Start time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    page_info = extract_page_info(filter_pages_with_title)
    total_pages = len(page_info)
    print(f"Total pages: {total_pages}")

    analytics_data = {}
    for index, (page_id, display_title, page_url) in enumerate(page_info, start=1):
        print(f"{index}/{total_pages}: {page_id} - {display_title} - {page_url}")
        analytics = get_page_analytics(page_id)
        analytics_data[page_id] = analytics
        time.sleep(random.uniform(0.5, 2.0))

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    print(f"End time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Duration: {duration}")

    save_to_json(analytics_data, f'raw/raw_analytics_filtered_{filter_pages_with_title}.json')

if __name__ == "__main__":
    main(filter_pages_with_title=True)
