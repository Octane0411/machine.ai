import csv
import time
import random
import json
import os
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Tuple
from playwright.sync_api import sync_playwright

class MajorCollector:
    def __init__(self, cache_file: str = "major_cache.json"):
        self.base_url = "https://liquipedia.net/counterstrike"
        self.cache_file = cache_file
        self.cache = self._load_cache()
        
        self.url_overrides = {
            "pasha": "pashaBiceps",
            "Edward": "Edward_(Ukrainian_player)",
            "AdreN": "AdreN_(Kazakh_player)",
            "karrigan": "karrigan",
            "dev1ce": "dev1ce",
            "f0rest": "f0rest",
            "GeT_RiGhT": "GeT_RiGhT",
            "kennyS": "kennyS",
            "olofmeister": "olofmeister",
            "GuardiaN": "GuardiaN",
            "Snax": "Snax",
            "shox": "shox",
            "KRIMZ": "KRIMZ",
            "flusha": "flusha",
            "JW": "JW",
            "Xyp9x": "Xyp9x",
            "dupreeh": "dupreeh",
            "gla1ve": "gla1ve",
            "magisk": "magisk",
            "electronic": "electronic",
            "Boombl4": "Boombl4",
            "Perfecto": "Perfecto",
            "b1t": "b1t",
            "m0NESY": "m0NESY",
            "donk": "donk",
            "Ax1Le": "Ax1Le",
            "sh1ro": "sh1ro",
            "nafany": "nafany",
            "Stewie2K": "Stewie2K",
            "twistzz": "Twistzz",
            "NAF": "NAF",
            "nitr0": "nitr0",
            "tarik": "tarik",
            "autimatic": "autimatic",
            "Skadoodle": "Skadoodle",
            "Hiko": "Hiko",
            "daps": "daps",
            "stanislaw": "stanislaw",
            "dycha": "dycha",
            "hades": "hades",
            "ropz": "ropz",
            "broky": "broky",
            "rain": "rain",
            "tabseN": "tabseN",
            "syrsoN": "syrsoN",
            "stavn": "stavn",
            "cadiaN": "cadiaN",
            "TeSeS": "TeSeS",
            "sjuush": "sjuush",
            "refrezh": "refrezh",
            "blameF": "blameF",
            "valde": "valde",
            "acoR": "acoR",
            "jabbi": "jabbi",
            "nicoodoz": "nicoodoz",
            "Spinx": "Spinx",
            "flamie": "flamie",
            "sdy": "sdy",
            "degster": "degster",
            "r1nkle": "r1nkle",
            "headtr1ck": "headtr1ck",
            "Mir": "Mir",
            "Jame": "Jame",
            "FL1T": "FL1T",
            "Qikert": "Qikert",
            "Buster": "Buster",
            "TaZ": "TaZ",
            "byali": "byali",
            "FalleN": "FalleN",
            "fer": "fer",
            "TACO": "TACO",
            "fnx": "fnx",
            "LUCAS1": "LUCAS1",
            "HEN1": "HEN1",
            "kscerato": "kscerato",
            "yuurih": "yuurih",
            "arT": "arT",
            "VINI": "VINI",
            "saffee": "saffee",
            "drop": "drop",
            "chelo": "chelo",
            "biguzera": "biguzera",
            "felps": "felps",
            "zews": "zews",
            "Boltz": "Boltz",
            "MalbsMd": "malbsMd",
            "chrisJ": "chrisJ",
            "woxic": "woxic",
            "XANTARES": "XANTARES",
            "Calyx": "Calyx",
            "MAJ3R": "MAJ3R",
            "nawwk": "nawwk",
            "Golden": "Golden",
            "REZ": "REZ",
            "Brollan": "Brollan",
            "es3tag": "es3tag",
            "allu": "allu",
            "sergej": "sergej",
            "Aleksib": "Aleksib",
            "suNny": "suNny",
            "jks": "jks",
            "AZR": "AZR",
            "Gratisfaction": "Gratisfaction",
            "Liazz": "Liazz",
            "INS": "INS",
            "BnTeT": "BnTeT",
            "RUSH": "RUSH",
            "Ex6TenZ": "Ex6TenZ",
            "SmithZz": "SmithZz",
            "RpK": "RpK",
            "bodyy": "bodyy",
            "NBK": "NBK",
            "apEX": "apEX",
            "Happy": "Happy",
            "KioShiMa": "kioShiMa",
            "Zonic": "zonic",
            "dennis": "dennis",
            "Lekr0": "Lekr0",
            "MSL": "MSL",
            "smooya": "smooya",
            "Grim": "Grim",
            "floppy": "floppy",
            "oSee": "oSee",
            "junior": "junior",
            "ztr": "ztr",
            "frozen": "frozen",
            "huNter": "huNter-",
            "NertZ": "NertZ",
            "SunPayus": "SunPayus",
            "jL": "jL",
            "Summer": "Summer",
            "Starry": "Starry",
            "EliGE": "EliGE",
            "magixx": "magixx",
            "chopper": "chopper",
            "zont1x": "zont1x",
            "siuhy": "siuhy",
            "bLitz": "bLitz",
            "Techno": "Techno4K",
            "Senzu": "Senzu",
            "mzinho": "mzinho",
            "910": "910",
            "Wicadia": "Wicadia",
            "HeavyGod": "HeavyGod",
            "torzsi": "torzsi",
            "Jimpphat": "Jimpphat",
            "flameZ": "flameZ",
            "mezii": "mezii",
            "jottAAA": "jottAAA",
            "iM": "iM",
            "w0nderful": "w0nderful",
            "kyxsan": "kyxsan",
            "Maka": "Maka",
            "Staehr": "Staehr",
            "FL4MUS": "FL4MUS",
            "fame": "fame",
            "ICY": "ICY",
            "ultimate": "ultimate",
            "snow": "snow",
            "nqz": "nqz",
            "Tauson": "Tauson",
            "sl3nd": "sl3nd",
            "PR": "PR",
            "story": "story",
            "skullz": "skullz",
            "exit": "exit",
            "Lucaozy": "Lucaozy",
            "brnz4n": "brnz4n",
            "insani": "insani",
            "phzy": "phzy",
            "JBa": "JBa",
            "LNZ": "LNZ",
            "JDC": "JDC",
            "fear": "fear",
            "somebody": "somebody",
            "CYPHER": "CYPHER",
            "jkaem": "jkaem",
            "kaze": "kaze",
            "ChildKing": "ChildKing",
            "L1haNg": "L1haNg",
            "Attacker": "Attacker",
            "JamYoung": "JamYoung",
            "Jee": "Jee",
            "Mercury": "Mercury",
            "Moseyuh": "Moseyuh",
            "Westmelon": "Westmelon",
            "z4kr": "z4kr",
            "EmiliaQAQ": "EmiliaQAQ",
            "C4LLM3SU3": "C4LLM3SU3",
            "xertioN": "xertioN"
        }

    def _load_cache(self) -> Dict[str, int]:
        if os.path.exists(self.cache_file):
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)

    def get_player_url(self, player_name: str) -> str:
        search_name = self.url_overrides.get(player_name, player_name)
        return f"{self.base_url}/{search_name}/Results"

    def get_major_count(self, player_name: str, page) -> Tuple[int, str]:
        url = self.get_player_url(player_name)
        
        if player_name in self.cache and self.cache[player_name] != -1:
            return self.cache[player_name], url

        print(f"Fetching major count for {player_name} from {url}...")
        
        try:
            # Relaxed timeout and wait condition
            response = page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Wait for table
            try:
                page.wait_for_selector("table.wikitable", timeout=5000)
            except:
                # If no table found, maybe 404 or no results
                if "Page does not exist" in page.content():
                    print(f"  Warning: Page does not exist for {player_name}")
                    self.cache[player_name] = -1
                    self._save_cache()
                    return -1, url
            
            # Human-like behavior: Scroll a bit
            try:
                page.evaluate("window.scrollBy(0, 300)")
                time.sleep(0.5)
            except:
                pass

            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            
            major_count = self._parse_majors(soup)
            
            print(f"  Found {major_count} majors for {player_name}")
            self.cache[player_name] = major_count
            self._save_cache()
            return major_count, url
            
        except Exception as e:
            print(f"  Error fetching {player_name}: {e}")
            return -1, url

    def _parse_majors(self, soup: BeautifulSoup) -> int:
        major_count = 0
        tables = soup.find_all('table', class_='wikitable')
        
        processed_majors = set()
        
        for table in tables:
            rows = table.find_all('tr')
            for row in rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) < 7: # Need at least 7 columns based on analysis
                    continue
                
                try:
                    # Updated indices based on HTML analysis:
                    # 0: Date
                    # 1: Place
                    # 2: Tier
                    # 3: Type
                    # 4: Game Icon
                    # 5: Tournament Icon
                    # 6: Tournament Name
                    
                    tier_text = cells[2].get_text().strip()
                    tournament_text = cells[6].get_text().strip()
                    
                    if "Major" in tournament_text:
                        if any(x in tournament_text for x in ["Qualifier", "RMR", "Showmatch", "Qual", "Minors", "Road to Rio", "ESL Major League", "Regional Major Rankings"]):
                            continue
                        
                        tier_link = cells[2].find('a')
                        is_s_tier = False
                        if (tier_link and "S-Tier" in tier_link.get('title', '')) or "S-Tier" in tier_text:
                            is_s_tier = True
                        
                        if not is_s_tier:
                            # Double check for other non-S-Tier majors if any
                            pass
                        
                        if tournament_text not in processed_majors:
                            processed_majors.add(tournament_text)
                            major_count += 1
                            
                except IndexError:
                    continue
                    
        return major_count

    def process_csv(self, input_file: str, output_file: str):
        players = []
        with open(input_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        header = lines[0].strip().split(',')
        print(f"Processing {len(lines)-1} players from {input_file}...")
        
        new_data = []
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={'width': 1920, 'height': 1080}
            )
            page = context.new_page()
            
            for line in lines[1:]:
                parts = line.strip().split(',')
                if len(parts) < 5:
                    continue
                    
                name = parts[0]
                team = parts[1]
                nationality = parts[2]
                age = parts[3]
                role = parts[4]
                
                major_count, url = self.get_major_count(name, page)
                final_count = major_count if major_count >= 0 else 0
                
                new_data.append({
                    "name": name,
                    "team": team,
                    "nationality": nationality,
                    "age": age,
                    "role": role,
                    "major_appearances": final_count,
                    "source_url": url
                })
                
                # Conservative delay: 3 to 5 seconds
                delay = random.uniform(3.0, 5.0)
                time.sleep(delay)
                
            browser.close()
            
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            fieldnames = ["name", "team", "nationality", "age", "role", "major_appearances", "source_url"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in new_data:
                writer.writerow(row)
                
        print(f"Successfully wrote {len(new_data)} players to {output_file}")

if __name__ == "__main__":
    collector = MajorCollector()
    if os.path.exists("test_players.csv"):
        print("Running on test_players.csv...")
        collector.process_csv("test_players.csv", "test_players_with_majors.csv")
    else:
        collector.process_csv("players.csv", "players_with_majors.csv")