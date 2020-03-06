import json
import os
import time
import boto3

def try_ex(func):
    """
    Call passed in function in try block. If KeyError is encountered return None.
    This function is intended to be used to safely access dictionary.

    Note that this function would have negative impact on performance.
    """

    try:
        return func()
    except KeyError:
        return None


def greeting(event):
    response = {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': 'Hey there! How is it going?'
            },
        }
    }
    return response
    

def thankyou(event):
    response = {
        'dialogAction': {
            'type': 'Close',
            'fulfillmentState': 'Fulfilled',
            'message': {
                'contentType': 'PlainText',
                'content': 'Always a pleasure!'
            },
        }
    }
    return response
    
def dine(event):
    location = try_ex(lambda: event['currentIntent']['slots']['Location'])
    cuisine = try_ex(lambda: event['currentIntent']['slots']['Cuisine'])
    party = try_ex(lambda: event['currentIntent']['slots']['PartySize'])
    date = try_ex(lambda: event['currentIntent']['slots']['Date'])
    dining_time = try_ex(lambda: event['currentIntent']['slots']['DiningTime'])
    phone = try_ex(lambda: event['currentIntent']['slots']['PhoneNumber'])
    
    session_attributes = event['sessionAttributes'] if event['sessionAttributes'] is not None else {}
    
    reservation = json.dumps({
        'Location': location,
        'Cuisine': cuisine,
        'PartySize': party,
        'Date': date,
        'DiningTime': dining_time,
        'PhoneNumber': phone
    })
    
    session_attributes['currentReservation'] = reservation
    
    # Execute as long as chatbot is still filling up slots
    if event['invocationSource'] == 'DialogCodeHook':
        
        #### Validating Cuisine
        cuisines_supported = ["indian", "mexican", "european", "japanese", "chinese"]
        
        cuisine = try_ex(lambda: event['currentIntent']['slots']['Cuisine'])
        
        
        if str(cuisine).lower() not in cuisines_supported and cuisine is not None:
            slots = event['currentIntent']['slots']
            validation_result = {
                'isValid': False,
                'violatedSlot': 'Cuisine',
                'message': {'contentType': 'PlainText', 'content': 'We currently only support New York!'}
            }
            slots['Cuisine'] = None
            response = {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'Cuisine',
                    'message': {'contentType': 'PlainText', 'content': 'We currently only support Indian, Mexican, European, Japanese and Chinese Cuisines'}
                    
                }
            }
            return response
            
        #### Validating City
        location = try_ex(lambda: event['currentIntent']['slots']['Location'])
            
        if str(location).lower() != "new york" and location is not None:
            slots = event['currentIntent']['slots']
            slots['Location'] = None
            
            response = {
                'sessionAttributes': session_attributes,
                'dialogAction': {
                    'type': 'ElicitSlot',
                    'intentName': event['currentIntent']['name'],
                    'slots': slots,
                    'slotToElicit': 'Location',
                    'message': {'contentType': 'PlainText', 'content': 'We currently only support New York'}
                    
                }
            }
            return response
            
            
            
            
        #### Delegating if everything is going smoothly
        
        response = {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate',
                'slots': event['currentIntent']['slots']
            }
        }
        
        return response
        
        
        
        
    # Execute when all slots are filled
    if event['invocationSource'] == 'FulfillmentCodeHook':
        
        try_ex(lambda: session_attributes.pop('currentReservation'))
        session_attributes['lastConfirmedReservation'] = reservation
        
        # Create SQS client
        sqs = boto3.client('sqs')
        
        queue_url = 'https://sqs.us-east-1.amazonaws.com/930401753392/Q1'
        
        # Send message to SQS queue
        responseSQS = sqs.send_message(
            QueueUrl=queue_url,
            DelaySeconds=10,
            MessageBody = (
                json.dumps({
                    'Location': location,
                    'Cuisine': cuisine,
                    'PartySize': party,
                    'Date': date,
                    'DiningTime': dining_time,
                    'PhoneNumber': phone
                })
            )
        )
        
        print("MessageID")
        print(responseSQS['MessageId'])
        
        message = "You're all set! " + cuisine + " cuisine suggestions at " + location + " will be sent to your phone shortly. Have a great day!" 
        
        response = {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close',
                'fulfillmentState': 'Fulfilled',
                'message': {
                    'contentType': 'PlainText',
                    'content': message
                },
            }
        }
        return response


def dispatch(event):
    intent_name = event['currentIntent']['name']
    
    if intent_name == "GreetingIntent":
        return greeting(event)
    elif intent_name == "ThankYouIntent":
        return thankyou(event)
    elif intent_name == "DiningSuggestionsIntent":
        return dine(event)
        
    raise Exception('Intent with name ' + intent_name + ' not supported')

def lambda_handler(event, context):
    # TODO implement
    
    return dispatch(event)