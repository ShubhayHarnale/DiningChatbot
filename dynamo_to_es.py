import boto3
from requests_aws4auth import AWS4Auth
from elasticsearch import Elasticsearch, RequestsHttpConnection

dynamodb = boto3.resource('dynamodb')

yelp_restaurants = dynamodb.Table('yelp-restaurants')
response = yelp_restaurants.scan()
data = response['Items']

while response.get('LastEvaluatedKey'):
    response = yelp_restaurants.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
    data.extend(response['Items'])

print(len(data))

session = boto3.session.Session()
credentials = session.get_credentials()
service = 'es'
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, session.region_name, service)
endpoint = "https://search-restaurants-ccwjaawlwnwrn73n7v5j3rf2sm.us-east-1.es.amazonaws.com"

es = Elasticsearch(
    endpoint,
    http_auth=awsauth,
    use_ssl=True,
    verify_certs=True,
    connection_class=RequestsHttpConnection
)
print(es.info())
count = 0
for restaurant in data:
    restaurantID = restaurant['id']
    cuisine = restaurant['cuisine']

    document = {
        'RestaurantID': restaurantID,
        'cusisine': cuisine
    }

    count += 1
    es.index(index='restaurants', doc_type='restaurant', id = restaurantID,body=document)

    check = es.get(index='restaurants',doc_type='restaurant', id = restaurantID)
    if check:
        print("Index %s found"%restaurantID)
        print(count)