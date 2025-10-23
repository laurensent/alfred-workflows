#!/usr/bin/env python3
import sys
import os
import subprocess
from leetcode_spider import LeetCodeSpider
from cache_manager import CacheManager

def send_notification(title, message, subtitle=""):
    """Send macOS notification"""
    try:
        cmd = ['osascript', '-e', f'display notification "{message}" with title "{title}"']
        if subtitle:
            cmd = ['osascript', '-e', f'display notification "{message}" with title "{title}" subtitle "{subtitle}"']
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError:
        print(f"Notification failed: {title} - {message}", file=sys.stderr)

def main():
    """Main update function"""
    if len(sys.argv) < 2:
        print("Usage: python3 update_handler.py <action>", file=sys.stderr)
        return 1

    action = sys.argv[1]
    spider = LeetCodeSpider()
    cache_manager = CacheManager()

    try:
        if action == "update_now":
            # Manual/forced update
            print("Starting update...", file=sys.stderr)
            send_notification("LeetCode Alfred", "Downloading problem data...", "Update Started")

            if spider.update_problems():
                status = cache_manager.get_cache_status()
                send_notification("LeetCode Alfred",
                                f"Update complete! {status['total_problems']} problems available",
                                "Ready to search")
                print("Update completed", file=sys.stderr)
                return 0
            else:
                send_notification("LeetCode Alfred", "Update failed. Check network connection", "Update Error")
                print("Update failed", file=sys.stderr)
                return 1

        else:
            print(f"Unknown action: {action}", file=sys.stderr)
            return 1

    except Exception as e:
        error_msg = str(e)
        send_notification("LeetCode Alfred", f"Update error: {error_msg}", "System Error")
        print(f"Update exception: {error_msg}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())