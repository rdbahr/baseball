import os
import requests
import statsapi

# 1. Create a directory to hold the logos
download_dir = "baseball_logos"
os.makedirs(download_dir, exist_ok=True)

print(f"📁 Created folder: {download_dir}/")

# 2. Download MLB Logos (Official CDN)
print("\n⚾ Downloading MLB Logos...")
mlb_teams = statsapi.get('teams', {'sportId': 1, 'activeStatus': 'Yes'})['teams']

for team in mlb_teams:
    team_id = team['id']
    team_name = team['name']
    url = f"https://www.mlbstatic.com/team-logos/team-cap-on-dark/{team_id}.svg"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filepath = os.path.join(download_dir, f"{team_id}.svg")
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  ✅ Saved {team_name} ({team_id}.svg)")
        else:
            print(f"  ⚠️ Failed to find logo for {team_name}")
    except Exception as e:
        print(f"  ❌ Error downloading {team_name}: {e}")

# 3. Download NPB Logos (From the Giants' Website workaround)
print("\n🎏 Downloading NPB Logos...")

# Since the Giants site uses English names instead of IDs, we have to map them to 
# the actual API IDs so they match your Elasticsearch script perfectly.
npb_mappings = {
    "giants": 137,     # Yomiuri Giants
    "tigers": 138,     # Hanshin Tigers
    "dragons": 136,    # Chunichi Dragons
    "swallows": 139,   # Tokyo Yakult Swallows
    "carp": 134,       # Hiroshima Toyo Carp
    "baystars": 133,   # Yokohama DeNA BayStars
    "buffaloes": 142,  # Orix Buffaloes
    "hawks": 144,      # Fukuoka SoftBank Hawks
    "lions": 143,      # Saitama Seibu Lions
    "eagles": 140,     # Tohoku Rakuten Golden Eagles
    "fighters": 141,   # Hokkaido Nippon-Ham Fighters
    "marines": 135     # Chiba Lotte Marines
}

for team_name, team_id in npb_mappings.items():
    url = f"https://www.giants.jp/icons/team/icon_{team_name}.svg"
    
    try:
       # Send a full suite of headers to trick the firewall
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
            'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.giants.jp/'
        }
        response = requests.get(url, headers=headers) 
        if response.status_code == 200:
            filepath = os.path.join(download_dir, f"{team_id}.svg")
            with open(filepath, 'wb') as f:
                f.write(response.content)
            print(f"  ✅ Saved {team_name.title()} ({team_id}.svg)")
        else:
            print(f"  ⚠️ Failed to find logo for {team_name.title()}")
    except Exception as e:
        print(f"  ❌ Error downloading {team_name.title()}: {e}")

print(f"\n🎉 All done! Check the '{download_dir}' folder on your PC.")
