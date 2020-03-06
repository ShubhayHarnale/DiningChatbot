import json
import boto3
from botocore.vendored import requests
from boto3.dynamodb.conditions import Key, Attr
import random

def lambda_handler(event, context):
    
    # Table 
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('yelp-restaurants')
    
    # SNS
    client = boto3.client("sns")
    
    
    # Getting data given by user
    message = event['Records'][0]['body']
    message = json.loads(message)
    cuisine = message["Cuisine"]
    party = message["PartySize"]
    time = message["DiningTime"]
    phone = "+1" + message["PhoneNumber"]
    date = message["Date"]
    print("CUISINE:  " + cuisine)
    
    # Getting data from ES
    url = "https://search-restaurants-ccwjaawlwnwrn73n7v5j3rf2sm.us-east-1.es.amazonaws.com/_search?q='{}'&size=1000".format(cuisine)
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    response = json.loads(response.text)
    
    # Getting data from DynamoDB
    message = "Hello! Here are my " + str(cuisine) + " suggestions for " + str(party) + " people, for " + str(date) + " at " + str(time) + ": "
    counter = 1
    
    total_count = response["hits"]["total"]["value"]
    
            
    while(counter < 4):
        rest = response["hits"]["hits"][random.randrange(0, total_count-1)]
        table_response = table.query(KeyConditionExpression=Key('id').eq(rest["_id"]))
        for i in table_response['Items']:
            m = str(counter) + "." + str(i["name"]) + " located at " + str(i["address"]) + "\n"
            message = message + m
            counter = counter + 1
    
    message = message + "Enjoy your meal!"
    print(phone)
    print(message)
    
    # Sending message
    client.publish(PhoneNumber = phone, Message = message) 
    
    
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
