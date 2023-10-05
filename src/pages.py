import requests
from settings import config

from utils import save_to_json

headers = {
    "Authorization": f"Bearer {config.TOKEN}",
    "Notion-Version": "2022-06-28"
}

def search_pages(cursor=None):
    data = {
        "filter": {
            "value": "page",
            "property": "object"
        },
        "page_size": 100
    }
    if cursor:
        data['start_cursor'] = cursor
    response = requests.post("https://api.notion.com/v1/search", headers=headers, json=data)
    return response.json()

# TODO check why its not getting all pages
def get_all_pages():
    all_pages = []
    response_json = search_pages()
    all_pages.extend(response_json['results'])
    while 'next_cursor' in response_json and response_json['next_cursor']:
        response_json = search_pages(response_json['next_cursor'])
        all_pages.extend(response_json['results'])
    return all_pages


def main():
    all_pages = get_all_pages()
    save_to_json(all_pages, 'pages.json')

if __name__ == "__main__":
    main()
