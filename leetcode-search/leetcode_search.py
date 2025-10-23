import os
import re
import sys
import json
import threading
from cache_manager import CacheManager
from leetcode_spider import LeetCodeSpider
from utils import get_data_dir, load_json_file


class LeetCodeSearch:
    def __init__(self):
        self.data_dir = get_data_dir()
        self.result_file = self.data_dir / 'result.json'
        self.cache_manager = CacheManager()
        self.spider = LeetCodeSpider()

    def check_and_update_cache_async(self):
        def update_worker():
            try:
                if self.cache_manager.should_update_cache():
                    print("🔄 Refreshing cache in the background...", file=sys.stderr)
                    self.spider.update_problems()
            except Exception as e:
                print(f"❌ Background update failed: {e}", file=sys.stderr)

        update_thread = threading.Thread(target=update_worker, daemon=True)
        update_thread.start()

    def load_problems_data(self):
        if not self.cache_manager.is_cache_available():
            print("🔄 First run detected, initializing data...", file=sys.stderr)
            if not self.spider.update_problems():
                return []
        return load_json_file(self.result_file, [])

    def search_problems(self, query):
        query = query.strip()

        # Handle lcupdate command
        if query == "lcupdate":
            return self.handle_manual_update()

        # Check if update is in progress first
        cache_info = self.cache_manager.get_cache_info()
        if cache_info.get('update_status') == 'updating':
            return self.handle_update_in_progress()

        # Check if cache needs update (first time or expired)
        if self.cache_manager.should_update_cache():
            return self.handle_update_needed()

        # Load and search data
        data = self.load_problems_data()
        if not data:
            return self.create_error_result("No data available")

        if not query:
            # Show first 50 problems when no query
            return self.show_all_problems(limit=50)

        search_pattern = '.*' + '.*'.join(query.split()) + '.*'
        result = []

        for item in data:
            if not re.search(search_pattern.lower(), item['titleCN'].lower() + item['titleUS'].lower()):
                continue

            search_item = item.copy()
            search_item['icon'] = {'path': 'icon.png'}
            keyword = os.environ.get('alfred_workflow_keyword', 'lc').lower()

            if keyword == 'lc':
                search_item['title'] = search_item['titleCN']
                search_item['subtitle'] = search_item['subtitleCN']
                search_item['arg'] = f"https://leetcode.cn/problems/{item['arg']}/description/"
            elif keyword == 'lcm':
                search_item['title'] = search_item['titleUS']
                search_item['subtitle'] = search_item['subtitleUS']
                search_item['arg'] = f"https://leetcode.com/problems/{item['arg']}/description/"

            result.append(search_item)

        if not result:
            return self.create_no_results(query)
        return {'items': result}

    def show_all_problems(self, limit=50):
        """Display all problems with an optional limit."""
        data = self.load_problems_data()
        if not data:
            return self.create_error_result("Unable to load problem data")

        result = []
        keyword = os.environ.get('alfred_workflow_keyword', 'lc').lower()

        for item in data[:limit]:  # Display only the first N problems to avoid overload
            search_item = item.copy()
            search_item['icon'] = {'path': 'icon.png'}

            if keyword == 'lc':
                search_item['title'] = search_item['titleCN']
                search_item['subtitle'] = search_item['subtitleCN']
                search_item['arg'] = f"https://leetcode.cn/problems/{item['arg']}/description/"
            elif keyword == 'lcm':
                search_item['title'] = search_item['titleUS']
                search_item['subtitle'] = search_item['subtitleUS']
                search_item['arg'] = f"https://leetcode.com/problems/{item['arg']}/description/"

            result.append(search_item)

        return {'items': result}

    def handle_manual_update(self):
        """Handle manual update command"""
        status = self.cache_manager.get_cache_status()
        last_update = status['last_update']

        if last_update:
            import datetime
            try:
                update_time = datetime.datetime.fromisoformat(last_update)
                time_str = update_time.strftime('%Y-%m-%d %H:%M')
                days_ago = status['days_since_update']
                relative_time = f"{days_ago} days ago" if days_ago is not None else "unknown"
            except:
                time_str = "parse failed"
                relative_time = "unknown"
        else:
            time_str = "never"
            relative_time = "never"

        auto_update = "enabled" if status['auto_update_enabled'] else "disabled"

        items = [{
            'title': "Cache Configuration",
            'subtitle': f"Interval: {status['update_interval']} days | Auto-update: {auto_update}",
            'arg': "",
            'icon': {'path': 'icon.png'}
        }, {
            'title': "Last Update Info",
            'subtitle': f"Time: {time_str} ({relative_time}) | Problems: {status['total_problems']}",
            'arg': "",
            'icon': {'path': 'icon.png'}
        }, {
            'title': "Update Now",
            'subtitle': "Force update all problem data",
            'arg': "update_now",
            'icon': {'path': 'icon.png'}
        }]

        return {'items': items}

    def handle_update_needed(self):
        """Handle when cache update is needed (first time or expired)"""
        status = self.cache_manager.get_cache_status()

        if not status['available']:
            message = "No data found. Press Enter to download problems."
        else:
            message = "Data expired. Press Enter to update problems."

        return {
            'items': [{
                'title': "Update Required",
                'subtitle': message,
                'arg': "start_update",
                'icon': {'path': 'icon.png'}
            }]
        }

    def handle_update_in_progress(self):
        """Handle when update is currently in progress"""
        return {
            'items': [{
                'title': "Update in Progress...",
                'subtitle': "Downloading problem data. Please wait for notification.",
                'arg': "",
                'icon': {'path': 'icon.png'}
            }]
        }

    def create_cache_status_result(self):
        status = self.cache_manager.get_cache_status()
        if not status['available']:
            return self.create_error_result("Cache unavailable. Please wait for initialization to finish.")

        last_update = status['last_update']
        if last_update:
            import datetime
            try:
                update_time = datetime.datetime.fromisoformat(last_update)
                time_str = update_time.strftime('%Y-%m-%d %H:%M')
            except:
                time_str = "unknown"
        else:
            time_str = "never updated"

        status_emoji = "✅" if not status['expired'] else "⏰"
        auto_update = "Enabled" if status['auto_update_enabled'] else "Disabled"

        items = [{
            'title': f"{status_emoji} Cache status",
            'subtitle': f"Total problems: {status['total_problems']} | Last update: {time_str}",
            'arg': "",
            'icon': {'path': 'icon.png'}
        }, {
            'title': "⚙️ Configuration",
            'subtitle': f"Update interval: {status['update_interval']} days | Auto-update: {auto_update}",
            'arg': "",
            'icon': {'path': 'icon.png'}
        }]

        if status['expired']:
            items.append({
                'title': "🔄 Manual cache refresh",
                'subtitle': "Press Enter to refresh problem data now",
                'arg': "lcupdate",
                'icon': {'path': 'icon.png'}
            })

        return {'items': items}

    def create_error_result(self, message):
        return {
            'items': [{
                'title': "Error",
                'subtitle': message,
                'arg': "",
                'icon': {'path': 'icon.png'}
            }]
        }

    def create_no_results(self, query):
        return {
            'items': [{
                'title': "No matching problems found",
                'subtitle': f"Query: {query}. Try different keywords",
                'arg': "",
                'icon': {'path': 'icon.png'}
            }]
        }


def main():
    if len(sys.argv) < 2:
        query = ""
    else:
        query = ' '.join(sys.argv[1:])

    # Handle update operations
    if query in ["update_now", "start_update"]:
        import subprocess
        try:
            # Start background update process
            subprocess.Popen([
                'python3',
                os.path.join(os.path.dirname(__file__), 'update_handler.py'),
                "update_now"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Return updating status
            result = {
                'items': [{
                    'title': "Updating problem data...",
                    'subtitle': "You will receive a notification when complete",
                    'arg': "",
                    'icon': {'path': 'icon.png'}
                }]
            }
        except Exception as e:
            result = {
                'items': [{
                    'title': "Update failed to start",
                    'subtitle': f"Error: {str(e)}",
                    'arg': "",
                    'icon': {'path': 'icon.png'}
                }]
            }
    else:
        search = LeetCodeSearch()
        result = search.search_problems(query)

    alfred_json = json.dumps(result, indent=2, ensure_ascii=False)
    sys.stdout.write(alfred_json)


if __name__ == "__main__":
    main()
