import subprocess
import sys

required_modules = ["base64", "json", "math", "decimal", "requests", "colorama"]

installables = ["requests", "colorama"]

for module in installables:
    try:
        __import__(module)
    except ImportError:
        print(f"'{module}' not found... installing it now")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module])

import base64
import json
import math
from decimal import Decimal
import requests
from colorama import Fore, Style


SHORTHAND_MULTIPLIERS = {"k": 1_000, "m": 1_000_000, "b": 1_000_000_000}


def parse_shorthand(stat_str: str):
    try:
        return int(stat_str)
    except ValueError:
        num = Decimal(stat_str[:-1])
        multiplier = SHORTHAND_MULTIPLIERS.get(stat_str[-1].lower(), 1)
        result = num * Decimal(multiplier)
        return int(result) if result == result.to_integral_value() else float(result)


def calculate_fairfight(attacker_score, defender_score):
    return 1 + ((8 / 3) * (defender_score / attacker_score))


encoded_data = input(
    "Paste the data string here (Make sure you ran the scraper script with BSP set to Battle Stat Score rather than Total Battle Stats): "
)
opponents = json.loads(base64.b64decode(encoded_data))

api_key = input("Enter your limited access key here: ").strip()
response = requests.get(
    f"https://api.torn.com/v2/user?selections=battlestats&key={api_key}"
)

if response.status_code != 200:
    print("Error: Couldn't fetch data from Torn API.")
    exit(1)

user_stats = response.json()
user_score = int(
    sum(
        map(
            math.sqrt,
            [
                user_stats["strength"],
                user_stats["speed"],
                user_stats["dexterity"],
                user_stats["defense"],
            ],
        )
    )
)

print(f"\nYour Battle Stat Score: {user_score}")


valid_targets = []
for opponent in opponents:
    opp_score = parse_shorthand(opponent["stats"])
    ff_value = calculate_fairfight(user_score, opp_score)

    if opp_score < user_score and ff_value > 2:
        valid_targets.append([opponent["name"], ff_value, opponent["playerid"]])

valid_targets.sort(key=lambda x: x[1], reverse=True)

print(f"\nYou have {len(valid_targets)} FairFight > 2 targets:\n")
max_name_len = max((len(name) for name, _, _ in valid_targets), default=0)

for i, (name, ff, id) in enumerate(valid_targets, 1):
    capped_ff = round(min(ff, 3), 2)
    if capped_ff == 3:
        color = Fore.GREEN
    elif capped_ff < 2.5:
        color = Fore.RED
    else:
        color = Fore.RESET

    print(
        f"{i:2}. {name.ljust(max_name_len)} | {color}{capped_ff:.2f}{Style.RESET_ALL} | https://www.torn.com/profiles.php?XID={id}"
    )
