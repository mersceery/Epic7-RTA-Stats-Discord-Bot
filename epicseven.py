import requests
import json

response = requests.get(
    "https://static.smilegatemegaport.com/gameRecord/epic7/epic7_user_world_global.json?_=1696281614568"
)

response_json = json.loads(response.text)

for nickname in response_json["users"]:
    if nickname["nick_nm"] == "Zernell":
        print(nickname["nick_no"])

import re
from collections import Counter

data = [
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c6062",""]',
    '"preban_list":["c2109",""]',
    '"preban_list":["c2109",""]',
]

extracted_values = []

# Regular expression pattern to match "c" followed by one or more digits within quotation marks
pattern = r'"(c\d+)"'

# Loop through the strings and extract values
for string in data:
    matches = re.findall(pattern, string)
    extracted_values.extend(matches)

# Print the extracted values
print(extracted_values)
value_counts = Counter(extracted_values)

# Print the counts of unique values
for value, count in value_counts.items():
    print(f"{value}: {count}")
