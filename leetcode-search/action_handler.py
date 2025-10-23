#!/usr/bin/env python3
import sys
import os
import subprocess

def main():
    if len(sys.argv) < 2:
        return 1

    action = sys.argv[1]

    # Handle update actions
    if action in ["start_update", "update_now"]:
        try:
            # Start background update process
            subprocess.Popen([
                'python3',
                os.path.join(os.path.dirname(__file__), 'update_handler.py'),
                "update_now"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print("Update started in background")
            return 0
        except Exception as e:
            print(f"Failed to start update: {e}")
            return 1

    # For other actions, treat as URL
    else:
        try:
            subprocess.run(['open', action], check=True)
            return 0
        except:
            return 1

if __name__ == "__main__":
    sys.exit(main())