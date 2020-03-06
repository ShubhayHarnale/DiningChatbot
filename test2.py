import json


data = {
    "Location": "new york",
    "Cuisine": "indian",
    "PartySize": "4",
    "Date": "2020-03-02",
    "DiningTime": "19:00",
    "PhoneNumber": "3473305867"
}

data = json.dumps(data)
data = json.loads(data)

print(data["Cuisine"])