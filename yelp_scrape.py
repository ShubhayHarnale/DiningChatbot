import requests
import pprint
import json
import decimal

pp = pprint.PrettyPrinter(indent=4)

url = "https://api.yelp.com/v3/businesses/search?location=Manhattan&categories=indpak, All&limit=50"

payload = {}
headers = {
  'Authorization': 'Bearer -u5npXAmutkqQyV-PxzVKJmuOIXPNAOJtypzTsgcNNIk2KB15L4tUJ-VELSylaqJVKEksxSBPo_WafCiVHdvmVBbOTb0K3wDaB3k-2WejV_XaDq83qo5K3Kp9WdYXnYx'
}

response = requests.request("GET", url, headers=headers, data = payload)

# print(response.text.encode('utf8'))

with open('test.json', 'w') as outf:
    outf.write(response.text)

pp.pprint(response.text)


# with open("test.json") as json_file:
# 	rest = json.load(json_file, parse_float = decimal.Decimal)
# 	rest = rest["businesses"]
# 	for r in rest:
# 		print(r)
