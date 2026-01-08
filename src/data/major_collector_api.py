import requests
import time
import csv
import os
import re
import json
from typing import Dict, List, Optional, Tuple

class MajorCollectorAPI:
    def __init__(self, email: str = "your_email@example.com", cache_file: str = "major_cache_api.json"):
        self.base_url = "https://liquipedia.net/counterstrike/api.php"
        self.cache_file = cache_file
        self.cache = self._load_cache()
        self.headers = {
            'User-Agent': f'CS_Guessing_Game_Data_Collector/1.0 ({email})',
            'Accept-Encoding': 'gzip'
        }
        
        self.url_overrides = {
            "pasha": "pashaBiceps",
            "Edward": "Edward_(Ukrainian_player)",
            "AdreN": "AdreN_(Kazakh_player)",
            # Add other overrides as needed
        }

    def _load_cache(self) -> Dict[str, int]:
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def get_major_count(self, player_name: str) -> int:
        if player_name in self.cache:
            return self.cache[player_name]

        search_name = self.url_overrides.get(player_name, player_name)
        # We query the /Results page
        title = f"{search_name}/Results"
        
        print(f"Fetching Wikitext for {title}...")
        
        params = {
            'action': 'query',
            'titles': title,
            'prop': 'revisions',
            'rvprop': 'content',
            'format': 'json'
        }
        
        try:
            # Rate limiting: 1 request per 2 seconds
            time.sleep(2.1)
            
            response = requests.get(self.base_url, headers=self.headers, params=params)
            
            if response.status_code == 403:
                print("  Error: 403 Forbidden. Check User-Agent or IP ban.")
                return -1
                
            response.raise_for_status()
            data = response.json()
            
            pages = data.get('query', {}).get('pages', {})
            content = ""
            for page_id, page_data in pages.items():
                if page_id == "-1":
                    print(f"  Page not found: {title}")
                    # Try main page if Results not found?
                    # For now just return 0 or -1
                    self.cache[player_name] = -1
                    self._save_cache()
                    return -1
                content = page_data.get('revisions', [{}])[0].get('*', '')
                
            major_count = self._parse_wikitext(content)
            print(f"  Found {major_count} majors for {player_name}")
            
            self.cache[player_name] = major_count
            self._save_cache()
            return major_count
            
        except Exception as e:
            print(f"  Error fetching {player_name}: {e}")
            return -1

    def _parse_wikitext(self, content: str) -> int:
        """
        Parse Wikitext to find Major appearances.
        Looks for rows in wikitable that contain "Major".
        """
        major_count = 0
        processed_majors = set()
        
        # Simple line-based parsing for wikitables
        # Rows start with |-
        # Cells separated by || or start with |
        
        # Regex to find tournament links like [[Tournament Name]] or [[Tournament Name|Display Name]]
        # We look for lines that contain "Major"
        
        lines = content.split('\n')
        for line in lines:
            # Check if line represents a row or cell content
            if "Major" in line:
                # Exclude Qualifiers, RMRs, etc.
                if any(x in line for x in ["Qualifier", "RMR", "Showmatch", "Qual", "Minors", "Road to Rio", "ESL Major League", "Regional Major Rankings"]):
                    continue
                
                # Check for S-Tier. In Wikitext, S-Tier is often linked [[S-Tier]] or just text
                # But the line might just be the tournament cell.
                # We need to be careful.
                
                # Robust way: Extract all links [[...]] in the line
                links = re.findall(r'\[\[([^\]]+)\]\]', line)
                
                for link in links:
                    # Link format: "Target" or "Target|Label"
                    parts = link.split('|')
                    target = parts[0]
                    label = parts[1] if len(parts) > 1 else target
                    
                    if "Major" in label or "Major" in target:
                        # Double check exclusions on the link text itself
                        if any(x in label for x in ["Qualifier", "RMR", "Showmatch", "Qual", "Minors"]):
                            continue
                            
                        # We assume if we found a valid Major link in a results table, it counts.
                        # Ideally we should check the "Tier" column, but that requires stateful parsing of the table.
                        # For a heuristic, this is often good enough if we exclude known non-majors.
                        
                        # Deduplicate
                        if target not in processed_majors:
                            processed_majors.add(target)
                            major_count += 1
                            
        return major_count

if __name__ == "__main__":
    # Use a dummy email for testing, but in production use a real one
    collector = MajorCollectorAPI(email="test_bot@example.com")
    
    print("Testing API collector on ZywOo...")
    count = collector.get_major_count("ZywOo")
    print(f"Result: {count}")