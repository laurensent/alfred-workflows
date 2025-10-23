import os
import json
import datetime
from pathlib import Path


def get_data_dir():
    """Return the workflow data directory path."""
    current_dir = Path(__file__).parent
    data_dir = current_dir / 'data'
    data_dir.mkdir(exist_ok=True)
    return data_dir


def load_json_file(file_path, default=None):
    """Safely load a JSON file and fall back to default when needed."""
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return default or {}
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading {file_path}: {e}")
        return default or {}


def save_json_file(file_path, data):
    """Safely persist JSON data to disk."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving {file_path}: {e}")
        return False


def get_days_since(date_str):
    """Calculate the number of days since the given ISO-formatted date."""
    try:
        target_date = datetime.datetime.fromisoformat(date_str)
        return (datetime.datetime.now() - target_date).days
    except (ValueError, TypeError):
        return float('inf')


def format_timestamp():
    """Return the current timestamp in ISO-8601 format."""
    return datetime.datetime.now().isoformat()


def is_valid_update_days(days):
    """Validate whether the update interval is within the supported range."""
    try:
        days = int(days)
        return 1 <= days <= 30
    except (ValueError, TypeError):
        return False
