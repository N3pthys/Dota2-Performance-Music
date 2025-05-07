import os
import time
import requests
import pandas as pd

# Base URL for OpenDota API (Free Tier - No Key Required)
BASE_URL = "https://api.opendota.com/api"
EXCEL_FILE = "test_data.xlsx"
MATCH_ID_FILE = "./match_ids.xlsx"  

# Function to fetch match data using Match ID
def fetch_match_data(match_id):
    url = f"{BASE_URL}/matches/{match_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Function to extract player data from match data
def extract_data(match_data):
    extracted_data = []
    
    for player in match_data.get("players", []):
        benchmarks = player.get("benchmarks", {})
        rank_tier = player.get("rank_tier")
        medal = {1: "Herald", 2: "Guardian", 3: "Crusader", 4: "Archon", 5: "Legend", 6: "Ancient", 7: "Divine", 8: "Immortal"}.get(rank_tier // 10, "Unknown") if rank_tier else "Unknown"
        
        win_or_lose = 1 if player.get("win", 0) > 0 else 0
        total_games = player.get("win", 0) + player.get("lose", 0)
        win_rate = (player.get("win", 0) / total_games) if total_games > 0 else 0
        
        extracted_data.append({
            "Match ID": match_data.get("match_id"),
            "Player ID": player.get("account_id"),
            "MMR": rank_tier,
            "Medal": medal,
            "WinOrLose": win_or_lose,
            "Win Rate": win_rate,
            "Role": {1: "Safe Lane", 2: "Mid Lane", 3: "Off Lane", 4: "Soft Support", 5: "Hard Support"}.get(player.get("lane_role"), "Unknown"),
            "GPMvsAVG": benchmarks.get("gold_per_min", {}).get("pct", 0),
            "XPMvsAVG": benchmarks.get("xp_per_min", {}).get("pct", 0),
            "KDAvsAVG": benchmarks.get("kda", {}).get("pct", 0),
            "DeathsVsAVG": benchmarks.get("deaths", {}).get("pct", 0),
            "AssistsVsAVG": benchmarks.get("assists", {}).get("pct", 0),
            "Supporting": int(player.get("purchase_tpscroll", 0) or 0) + 
                          int(player.get("obs_placed", 0) or 0) + 
                          int(player.get("sen_placed", 0) or 0),
            "Final Net Worth": player.get("total_gold", 0),
            "Game Duration": match_data.get("duration", 0) // 60,
            "Kills": player.get("kills"),
            "Deaths": player.get("deaths"),
            "Assists": player.get("assists"),
            "APM": player.get("actions_per_min"),
            "GPM": player.get("gold_per_min"),
            "XPM": player.get("xp_per_min"),
            "Pushing": (player.get("tower_damage") or 0) / 10,  # Scaled 0-10
	    "Fighting": (player.get("hero_damage") or 0) / 10,  # Scaled 0-10
	    "Farming": (player.get("gold_per_min") or 0) / 10     # Scaled 0-10
        })
    return extracted_data

# Function to save data to Excel
def save_to_excel(data):
    if os.path.exists(EXCEL_FILE):
        df_existing = pd.read_excel(EXCEL_FILE)
    else:
        df_existing = pd.DataFrame()

    df_new = pd.DataFrame(data)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["Match ID", "Player ID"], keep="last")
    
    df_combined.to_excel(EXCEL_FILE, index=False)
    print("Data saved successfully!")

# Main Execution
if __name__ == "__main__":
    df_match_ids = pd.read_excel(MATCH_ID_FILE)
    match_ids = df_match_ids.iloc[:, 0].astype(str).tolist()

    all_data = []
    start_time = time.time()
    
    for i, match_id in enumerate(match_ids):
        match_data = fetch_match_data(match_id)
        if match_data:
            all_data.extend(extract_data(match_data))
        else:
            print(f"Failed to fetch data for Match ID {match_id}")

        # Respect the API rate limit (60 calls per minute)
        if (i + 1) % 60 == 0:
            elapsed_time = time.time() - start_time
            if elapsed_time < 60:
                time.sleep(60 - elapsed_time)
            start_time = time.time()
    
    if all_data:
        save_to_excel(all_data)
