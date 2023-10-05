from collections import deque
from typing import List, Dict, Any, Optional, Union

from utils import load_from_json, save_to_json

def bfs_find_key_value(properties: Union[Dict[str, Any], List[Any]], key_to_find: str) -> Optional[str]:
    queue = deque([(properties, [])])
    
    while queue:
        current, path = queue.popleft()
        
        if isinstance(current, dict):
            for key, value in current.items():
                new_path = path + [key]
                if key == key_to_find:
                    return current[key]
                queue.append((value, new_path))
        elif isinstance(current, list):
            for index, value in enumerate(current):
                new_path = path + [index]
                queue.append((value, new_path))
    return None

def filter_entry(entry: Dict[str, Any]) -> Dict[str, Optional[Union[str, Dict[str, Any]]]]:
    filtered_entry = {}
    
    filtered_entry['id'] = entry.get('id', None)
    filtered_entry['created_time'] = entry.get('created_time', None)
    filtered_entry['last_edited_time'] = entry.get('last_edited_time', None)
    filtered_entry['url'] = entry.get('url', None)
    filtered_entry['parent'] = entry.get('parent', None)
    
    properties = entry.get('properties', {})
    title_field = properties.get('title', {})
    title_list = title_field.get('title', [])
    filtered_entry['page_title'] = title_list[0].get('plain_text', None) if title_list else None
    
    alternative_title_field = properties.get('Nome', properties.get('Name', {}))
    alternative_title_list = alternative_title_field.get('title', [])
    filtered_entry['alternative_title'] = alternative_title_list[0].get('plain_text', None) if alternative_title_list else None
    
    if filtered_entry['alternative_title'] is None:
        filtered_entry['alternative_title'] = bfs_find_key_value(properties, 'plain_text')
    
    return filtered_entry

if __name__ == "__main__":
    data = load_from_json('raw/raw_pages.json')
    
    filtered_data_with_titles_updated = [filter_entry(entry) for entry in data]
    
    save_to_json(filtered_data_with_titles_updated, 'parsed/parsed_pages.json')