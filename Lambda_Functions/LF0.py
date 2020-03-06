import json
import boto3

# def response(message, status_code):
#     return {
#         'statusCode': str(status_code),
#         'body': json.dumps(message),
#         'headers': {
#             'Content-Type': 'application/json',
#             'Access-Control-Allow-Origin': '*',
#             "Access-Control-Allow-Credentials" : True 
#         }
#     }

def lambda_handler(event, context):
    # TODO implement
    message = event["messages"][0]["unstructured"]["text"]
    print("MESSAGE from client: " + message)
    
    
    # message = json.dumps(message)
    
    # Call Lex Bot 
    client = boto3.client('lex-runtime')
    
    response = client.post_text(
        botName='DiningConcierge',
        botAlias='ChatbotAlias',
        userId='Chatbot',
        inputText=message
    )
    
    #response = json.dumps(response)
    print("MESSAGE from Chatbot: " + json.dumps(response))
    reply = response["message"]
    
    
    
    return {
        "messages": [
            {
                "type": "string",
                "unstructured": {
                    "id": "string",
                    "text": reply,
                    "timestamp": "string"
                }
            }
        ]
        
    }
    
    # return response({'message': message}, 200)