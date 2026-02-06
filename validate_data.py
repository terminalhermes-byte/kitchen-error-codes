#!/usr/bin/env python3
import json
import sys

def check_json():
    try:
        with open("errors.json", "r") as f:
            data = json.load(f)
        
        required_keys = ["manufacturer", "model", "code", "title", "cause", "fix"]
        
        for i, entry in enumerate(data):
            for key in required_keys:
                if key not in entry or not entry[key]:
                    print(f"❌ Error in entry #{i} ({entry.get('code', 'Unknown')}): Missing '{key}'")
                    return 1
        print("✅ errors.json passed validation.")
        return 0
    except Exception as e:
        print(f"❌ JSON Error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(check_json())
