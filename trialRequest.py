import requests
import json
import pandas as pd
import re
from collections import Counter


def calculate_mvp_percentage(total_mvp, total_match):
    return round((total_mvp / len(total_match)) * 100)


def calculate_prebans_percentage(total_mvp, total_match):
    return round((total_mvp / total_match) * 100)


def rta_stats(nickname):
    response = requests.get(
        "https://static.smilegatemegaport.com/gameRecord/epic7/epic7_user_world_global.json?_=1696281614568"
    )

    response_json = json.loads(response.text)
    result_battle = []
    all_my_decks = []
    most_common_picks = []
    preban_list = []

    username = nickname

    for nickname in response_json["users"]:
        if nickname["nick_nm"] == username:
            url = "https://epic7.gg.onstove.com/gameApi/getBattleList"
            querystring = {
                "nick_no": nickname["nick_no"],
                "world_code": "world_global",
                "lang": "en",
                "season_code": "",
            }

            headers = {
                "authority": "epic7.gg.onstove.com",
                "accept": "application/json, text/plain, */*",
                "accept-language": "en,en-US;q=0.9,de;q=0.8",
                "content-length": "0",
                "content-type": "application/x-www-form-urlencoded",
                "cookie": "NNTO=DE; PRM=en; LOCALE=EN; TZ=Europe/Berlin; TZ_OFFSET=120; REGULATION=GDPR; sgs_da_uuid=eac33b99-73fa-4880-93eb-26fe330525ac; sgs_da_session=eac33b99-73fa-4880-93eb-26fe330525ac; _ga_9Y2GLG717V=GS1.2.1696799350.2.1.1696799368.42.0.0; _ga_G9RYV7ZE9W=GS1.1.1696799343.2.1.1696799388.0.0.0; _ga=GA1.1.1136107383.1696279710; _ga_C6JZMC6VFJ=GS1.1.1697134932.2.1.1697135184.0.0.0; _ga_3NZYVSWQ6K=GS1.1.1697134932.3.1.1697135184.0.0.0; _ga_215JE0229Q=GS1.1.1697221540.6.1.1697221560.0.0.0",
                "origin": "https://epic7.gg.onstove.com",
                "referer": "https://epic7.gg.onstove.com/battlerecord/world_global/94566293",
                "sec-ch-ua": "^\^Chromium^^;v=^\^118^^, ^\^Google",
                "sec-ch-ua-mobile": "?1",
                "sec-ch-ua-platform": "^\^Android^^",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36",
            }

            response = requests.request(
                "POST", url, headers=headers, params=querystring
            )

            data = response.json()

            for battle in data["result_body"]["battle_list"]:
                iswin = battle.get("iswin")
                prebanList = battle.get("prebanList")
                result_battle.append(iswin)
                preban_list.append(prebanList)

                my_team_data = battle.get("my_deck", {}).get("hero_list", [])

                for hero in my_team_data:
                    hero_code = hero.get("hero_code")
                    mvp = hero.get("mvp", 0)
                    ban = hero.get("ban", 0)
                    first_pick = hero.get("first_pick", 0)

                    all_my_decks.append(
                        {
                            "hero_code": hero_code,
                            "mvp": mvp,
                            "ban": ban,
                            "first_pick": first_pick,
                        }
                    )

            url = "https://epic7.gg.onstove.com/gameApi/getUserInfoSeason"

            querystring = {
                "nick_no": nickname["nick_no"],
                "world_code": "world_global",
                "lang": "en",
                "search_type": "2",
                "season_code": "pvp_rta_ss11",
            }
            headers = {
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://epic7.gg.onstove.com/battlerecord/world_global/171975692",
                "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.188 Safari/537.36 CrKey/1.54.250320",
                "Content-Type": "application/x-www-form-urlencoded",
            }

            response_most_common_picks = requests.request(
                "POST", url, headers=headers, params=querystring
            )
            data2 = response_most_common_picks.json()
            for common_picks in data2["result_body"]["hero_list"]:
                win_rate = common_picks.get("win_rate")
                hero_code = common_picks.get("hero_code")

                most_common_picks.append(
                    {
                        "win_rate": win_rate,
                        "hero_code": hero_code,
                    }
                )

    df = pd.DataFrame(all_my_decks)
    hero_sum = (
        df.groupby("hero_code")
        .agg({"mvp": "sum", "ban": "sum", "first_pick": "sum"})
        .reset_index()
    )
    # specific_hero_code = "c1103"
    # mvp_sum_for_specific_hero = hero_sum.loc[
    #     hero_sum["hero_code"] == specific_hero_code, "mvp"
    # ].values[0]

    with open("heroes.json") as json_file:
        json_data = json.load(json_file)

    #############################
    sorted_df = hero_sum.sort_values(by="mvp", ascending=False)
    top_5_mvp_hero_pairs = sorted_df[["hero_code", "mvp"]].head(5)

    # print(mvp_sum_for_specific_hero)
    # print(hero_sum)
    # print(result_battle)
    most_common_picks_data = []
    most_mvp_char = []
    most_preban_char = []
    most_first_pick_char = []

    # Most common picks
    for picks in most_common_picks:
        for item in json_data["hero_name"]:
            if picks["hero_code"] in item:
                value = item[picks["hero_code"]]
                most_common_picks_data.append(f"{value} ({picks['win_rate']}%)")

    # Join the elements of the list into a single string with line breaks
    formatted_most_common_picks = "\n".join(most_common_picks_data)

    print(f"Most MVP Character within {len(result_battle)} Matches:")
    for index, row in top_5_mvp_hero_pairs.iterrows():
        hero_code = row["hero_code"]
        mvp = row["mvp"]
        # print(f"Hero Code: {hero_code}, MVP: {mvp}")

        for item in json_data["hero_name"]:
            if hero_code in item:
                value = item[hero_code]
                most_mvp_char.append(
                    f"{value} ({calculate_mvp_percentage(mvp, result_battle)}%)"
                )
                break

    formatted_most_mvp_char = "\n".join(most_mvp_char)

    extracted_values = []

    pattern = r'"(c\d+)"'

    for string in preban_list:
        matches = re.findall(pattern, string)
        extracted_values.extend(matches)

    value_counts = Counter(extracted_values)

    # sort n count in descending order
    sorted_value_counts = sorted(value_counts.items(), key=lambda x: x[1], reverse=True)
    total_prebans_per_matches = sum(count for value, count in sorted_value_counts)
    print(f"Most prebans Character within {len(result_battle)} Matches:")
    for value, count in sorted_value_counts:
        for item in json_data["hero_name"]:
            if value in item:
                value = item[value]
                print(
                    most_preban_char.append(
                        f"{value} ({calculate_prebans_percentage(count, total_prebans_per_matches)}%)"
                    )
                )
                break

    formatted_most_preban_char = "\n".join(most_preban_char)

    # Most first pick characters
    filtered_hero_sum = hero_sum[hero_sum["first_pick"] != 0]
    sorted_first_pick_df = filtered_hero_sum.sort_values(
        by="first_pick", ascending=False
    )
    top_5_first_pick_hero_pairs = sorted_first_pick_df[
        ["hero_code", "first_pick"]
    ].head(5)

    total_first_pick_sum = hero_sum["first_pick"].sum()

    print(f"Most first pick Character within {total_first_pick_sum} Matches:")

    for index, row in top_5_first_pick_hero_pairs.iterrows():
        hero_code = row["hero_code"]
        first_pick = row["first_pick"]
        # print(f"Hero Code: {hero_code}, MVP: {mvp}")

        for item in json_data["hero_name"]:
            if hero_code in item:
                value = item[hero_code]
                print(
                    most_first_pick_char.append(
                        f"{value} ({calculate_prebans_percentage(first_pick, total_first_pick_sum)}%)"
                    )
                )
                break

    formatted_most_first_pick_char = "\n".join(most_first_pick_char)

    yield formatted_most_common_picks
    yield len(result_battle)
    yield formatted_most_mvp_char
    yield formatted_most_preban_char
    yield total_first_pick_sum
    yield formatted_most_first_pick_char
