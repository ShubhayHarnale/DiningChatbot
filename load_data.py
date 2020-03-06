import requests
import pprint
import json
import decimal
import boto3

pp = pprint.PrettyPrinter(indent=4)

# dynamodb = boto3.resource('dynamodb', region_name='us-east-1', endpoint_url="https://dynamodb.us-east-1.amazonaws.com")

# table = dynamodb.Table('yelp-restaurants')

client = boto3.client('dynamodb')


with open("chinese_data.json") as json_file:
	rest = json.load(json_file, parse_float = decimal.Decimal)
	rest = rest["businesses"]
	for r in rest:
		if 'id' in r:
			id = r["id"]
		if 'name' in r:
			name = r["name"]
		if 'url' in r:
			url = r["url"]
		if 'rating' in r:
			rating = r["rating"]
		if 'coordinates' in r:
			lat = r["coordinates"]["latitude"]
			longi = r["coordinates"]["longitude"]
			coordinates = "latitude: " + str(lat) + ", longitude: " + str(longi)
		if 'price' in r:
			price = r["price"]
		if 'address1' in r['location']:
			address1 = r["location"]["address1"]
			if address1 is None:
				address1 = ""
		if 'address2' in r['location']:
			address2 = r["location"]["address2"]
			if address2 is None:
				address2 = ""
		if 'address3' in r['location']:
			address3 = r["location"]["address3"]
			if address3 is None:
				address3 = ""
		if 'city' in r['location']:
			city = r["location"]["city"]
		if 'zip_code' in r['location']:
			zipcode = r["location"]["zip_code"]
		if "review_count" in r:
			review_count = r["review_count"]
		if "categories" in r:
			cuisine = r["categories"][0]["title"]

		comb_address = str(address1) + " " + str(address2) + " " + str(address3)

		# print(id)
		# print(name)
		# print(rating)
		# print(address1)

		response = client.put_item(
			TableName='yelp-restaurants',
			Item = {
				'id': {"S": id},
				'name': {"S": name},
				'cuisine': {"S": cuisine},
				'url': {"S": url},
				'address': {"S": comb_address},
				'city': {"S": city},
				'zipcode': {"S": zipcode},
				'review_count': {"S": str(review_count)},
				'coordinates': {"S": coordinates}

			}
		)