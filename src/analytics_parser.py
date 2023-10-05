from typing import List, Dict, Any
from utils import load_from_json, save_to_json

def extract_page_data(page: Dict[str, Any], raw_analytics: Dict[str, Any]) -> List[Dict[str, Any]]:
    extracted_entries = []
    
    page_id = page.get('id')
    url = page.get('url')
    page_title = page.get('page_title')
    alternative_title = page.get('alternative_title')
    
    analytics_data: List[dict] = raw_analytics.get(str(page_id), [])
    
    for entry in analytics_data:
        new_entry = {
            'id': page_id,
            'url': url,
            'page_title': page_title,
            'alternative_title': alternative_title,
            'ds': entry.get('ds'),
            'unique_views': entry.get('unique_views'),
            'total_views': entry.get('total_views')
        }
        extracted_entries.append(new_entry)
    
    return extracted_entries

def main(filter_pages_with_title: bool):
    new_data = []
    
    raw_analytics = load_from_json(f'raw/raw_analytics_filtered_{filter_pages_with_title}.json')
    parsed_pages = load_from_json('parsed/parsed_pages.json')
    
    for page in parsed_pages:
        new_data.extend(extract_page_data(page, raw_analytics))
    
    save_to_json(new_data, f'parsed/parsed_analytics_filtered_{filter_pages_with_title}.json')

if __name__ == "__main__":
    main(filter_pages_with_title=True)
