import os
from utils import get_data_dir, load_json_file, save_json_file, is_valid_update_days


class ConfigManager:
    def __init__(self):
        self.data_dir = get_data_dir()
        self.config_file = self.data_dir / 'config.json'
        self.default_config = {
            'update_interval_days': 7,
            'auto_update_enabled': True,
            'last_manual_update': None,
            'version': '2.0'
        }

    def load_config(self):
        config = load_json_file(self.config_file, self.default_config.copy())
        if not is_valid_update_days(config.get('update_interval_days')):
            config['update_interval_days'] = self.default_config['update_interval_days']
        if 'auto_update_enabled' not in config:
            config['auto_update_enabled'] = self.default_config['auto_update_enabled']
        if 'version' not in config:
            config['version'] = self.default_config['version']
        return config

    def save_config(self, config):
        return save_json_file(self.config_file, config)

    def get_update_interval(self):
        config = self.load_config()
        return config.get('update_interval_days', self.default_config['update_interval_days'])

    def set_update_interval(self, days):
        if not is_valid_update_days(days):
            return False
        config = self.load_config()
        config['update_interval_days'] = int(days)
        return self.save_config(config)

    def is_auto_update_enabled(self):
        config = self.load_config()
        return config.get('auto_update_enabled', True)

    def set_auto_update(self, enabled):
        config = self.load_config()
        config['auto_update_enabled'] = bool(enabled)
        return self.save_config(config)

    def get_config_from_env(self):
        env_config = {}
        update_days = os.environ.get('UPDATE_DAYS')
        if update_days and is_valid_update_days(update_days):
            env_config['update_interval_days'] = int(update_days)
        auto_update = os.environ.get('AUTO_UPDATE', 'true').lower()
        env_config['auto_update_enabled'] = auto_update in ['true', '1', 'yes', 'on']
        return env_config

    def get_effective_config(self):
        config = self.load_config()
        env_config = self.get_config_from_env()
        config.update(env_config)
        return config