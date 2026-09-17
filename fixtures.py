import requests
import os
from collections import defaultdict
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ["FOOTBALL_DATA_KEY"]
NTFY_TOPIC = os.environ["NTFY_TOPIC"]

LEAGUES = "PL,PD,SA,BL1,FL1,CL"
LOCAL = ZoneInfo("America/Chicago")

LEAGUE_EMOJI = {
    "Premier League": "🏴󠁧󠁢󠁥󠁮󠁧󠁿",
    "Primera Division": "🇪🇸",
    "Serie A": "🇮🇹",
    "Bundesliga": "🇩🇪",
    "Ligue 1": "🇫🇷",
    "UEFA Champions League": "🏆",
}

today = datetime.now(LOCAL).date()
tomorrow = today + timedelta(days=1)

response = requests.get(
    "https://api.football-data.org/v4/matches",
    headers={"X-Auth-Token": API_KEY},
    params={
        "competitions": LEAGUES,
        "dateFrom": today.isoformat(),
        "dateTo": tomorrow.isoformat(),
    },
)
matches = response.json()["matches"]

by_league = defaultdict(list)
for m in matches:
    utc = datetime.fromisoformat(m["utcDate"].replace("Z", "+00:00"))
    local = utc.astimezone(LOCAL)
    if local.date() != today:
        continue
    by_league[m["competition"]["name"]].append({
        "time": local,
        "home": m["homeTeam"]["shortName"],
        "away": m["awayTeam"]["shortName"],
    })

count = sum(len(v) for v in by_league.values())

if count == 0:
    body = "No matches in your leagues today."
else:
    lines = []
    for league in sorted(by_league):
        lines.append(f"{LEAGUE_EMOJI.get(league, '')} {league}")
        for g in sorted(by_league[league], key=lambda x: x["time"]):
            t = g["time"].strftime("%I:%M %p").lstrip("0")
            lines.append(f"  {t}  {g['home']} vs {g['away']}")
        lines.append("")
    body = "\n".join(lines).strip()

title = f"{count} matches today" if count else "No matches today"

requests.post(
    f"https://ntfy.sh/{NTFY_TOPIC}",
    data=body.encode("utf-8"),
    headers={"Title": title, "Priority": "default", "Tags": "soccer, moneybag"},
)

print(title)
print(body)