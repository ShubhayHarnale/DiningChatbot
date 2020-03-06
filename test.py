import requests
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
import boto3



dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('yelp-restaurants')



url = "https://search-restaurants-ccwjaawlwnwrn73n7v5j3rf2sm.us-east-1.es.amazonaws.com/_search?q='chinese'"

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)


response = json.loads(response.text)

#print(response["hits"]["hits"][0]["_id"])

final_data = {}
data = {}
message = ""
counter = 1

for rest in response["hits"]["hits"]:
    #print(rest["_id"])
    table_response = table.query(KeyConditionExpression=Key('id').eq(rest["_id"]))
    for i in table_response['Items']:
        #print(i['id'] + ":" + i['name'])
        if counter > 3:
        	break
        m = str(counter) + "." + str(i["name"]) + " located at " + str(i["address"]) + "\n"
        message = message + m
        counter = counter+1
        


print(message)


