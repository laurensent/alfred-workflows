import os
from utils import get_data_dir, load_json_file, save_json_file, get_days_since, format_timestamp
from config_manager import ConfigManager


class CacheManager:
    def __init__(self):
        self.data_dir = get_data_dir()
        self.cache_info_file = self.data_dir / 'cache_info.json'
        self.result_file = self.data_dir / 'result.json'
        self.config_manager = ConfigManager()

    def get_cache_info(self):
        default_info = {
            'last_update': None,
            'total_problems': 0,
            'update_status': 'never',
            'version': '2.0',
            'error_message': None
        }
        return load_json_file(self.cache_info_file, default_info)

    def save_cache_info(self, info):
        return save_json_file(self.cache_info_file, info)

    def is_cache_expired(self):
        cache_info = self.get_cache_info()
        last_update = cache_info.get('last_update')
        if not last_update:
            return True
        config = self.config_manager.get_effective_config()
        update_interval = config.get('update_interval_days', 7)
        days_since_update = get_days_since(last_update)
        return days_since_update >= update_interval

    def is_cache_available(self):
        return os.path.exists(self.result_file) and os.path.getsize(self.result_file) > 0

    def should_update_cache(self):
        config = self.config_manager.get_effective_config()
        if not config.get('auto_update_enabled', True):
            return False
        if not self.is_cache_available():
            return True
        return self.is_cache_expired()

    def update_cache_info(self, total_problems=None, status='success', error_message=None):
        cache_info = self.get_cache_info()
        cache_info.update({
            'last_update': format_timestamp(),
            'update_status': status,
            'version': '2.0'
        })
        if total_problems is not None:
            cache_info['total_problems'] = total_problems
        if error_message:
            cache_info['error_message'] = error_message
        elif status == 'success':
            cache_info['error_message'] = None
        return self.save_cache_info(cache_info)

    def get_cache_status(self):
        cache_info = self.get_cache_info()
        config = self.config_manager.get_effective_config()
        last_update = cache_info.get('last_update')
        days_since_update = get_days_since(last_update) if last_update else None
        update_interval = config.get('update_interval_days', 7)
        status = {
            'available': self.is_cache_available(),
            'expired': self.is_cache_expired(),
            'last_update': last_update,
            'days_since_update': days_since_update,
            'update_interval': update_interval,
            'total_problems': cache_info.get('total_problems', 0),
            'auto_update_enabled': config.get('auto_update_enabled', True),
            'update_status': cache_info.get('update_status', 'never'),
            'error_message': cache_info.get('error_message')
        }
        return status