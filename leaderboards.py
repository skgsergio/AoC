import json
import requests

from zoneinfo import ZoneInfo
from datetime import datetime


def leaderboard(leaderboard_id: int, year: int, session: str, tz: ZoneInfo) -> str:
    output = ""

    res = requests.get(
        f"https://adventofcode.com/{year}/leaderboard/private/view/{leaderboard_id}.json",
        cookies = {
            "session": session
        },
    )

    leaderboard = res.json()

    for m in sorted(leaderboard["members"].values(), key=lambda m: m["local_score"], reverse=True):
        output += f"\N{bust in silhouette} {m['name']} \N{hundred points symbol} {m['local_score']}\n"

        for day, stars in sorted(m["completion_day_level"].items(), key=lambda c: int(c[0])):
            s1 = datetime.fromtimestamp(stars["1"]["get_star_ts"], tz)
            s2 = datetime.fromtimestamp(stars["2"]["get_star_ts"], tz) if "2" in stars else None

            day_str = f"    Day {day}: \N{white medium star} {s1.isoformat()}"

            if s2:
                day_str += f" \N{white medium star}\N{white medium star} {s2.isoformat()}"
                day_str += f" \N{timer clock} {s2 - s1}"

            output += f"{day_str}\n"

    return output


if __name__ == "__main__":
    with open("leaderboards.json") as f:
        config = json.loads(f.read())

    tz = ZoneInfo(config["tz"])

    for name, l in config["leaderboards"].items():
        fname = f"leaderboard_{name}.txt"

        print(f"Retrieving {name} and saving it as {fname}")

        with open(fname, "w") as f:
            f.write(leaderboard(l["id"], l["year"], l["session"], tz))
