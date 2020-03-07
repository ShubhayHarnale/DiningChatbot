# [Dining Concierge chatbot](http://diningconciergechatbot.s3-website-us-east-1.amazonaws.com/)


This chatbot, dubbed "BATMAN", is designed to provide dining recommendations. The recommendation process can be invoked by sending messages like "I need some restaurant suggestions", "Need help finding a restaurant", etc.


# Sample Conversation

Markdown is a lightweight markup language based on the formatting conventions that people naturally use in email.  As [John Gruber] writes on the [Markdown site][df1]

> Bot: Hello there!  
> User: Hi  
> Bot: Hey there! How is it going?  
> User: I am hungry
> Bot: I can help with that! What city are you looking to dine in?
> User: New York
> Bot: What cuisine would you like to try today?
> User: Indian
> Bot: How many people are in your party?
> User: 4
> Bot: What date?
> User: Tomorrow
> Bot: At what time would you like to dine?
> User: 7 PM
> Bot: Lastly, I need your phone number so I can send you my findings.
> User: 3473305867
> Bot: You're all set! Indian cuisine suggestions at New York will be sent to your phone shortly. Have a great day!

The User then receives the following text on his/her mobile phone:

"Hello! Here are my Indian suggestions for 4 people, for 2020-03-07 at 19:00: 
1.deep indian kitchen - indikitch located at 940 8th Ave  
2.NY Dosas located at 50 Washington Sq S  
3.Samossa Bites located at 35-27 31st St  
Enjoy your meal!"

### Files

| Plugin | README |
| ------ | ------ |
| yelp_scrape.py | Script scrapes Restaurants of each cuisine |
| dynamo_to_es.py | Loads data from DynamoDB to Elastic Search|
| load_data.py | Reads the scraped restaurant JSON data and loads it in DynamoDB |
| index.html | Main HTML file |
| *.json | Each of these files contain the scraped restaurant data for each cuisine |

###### The folder "Lambda_Functions" contains LF0, LF1 and LF2. All 3 functions have been designed according to the assignment given in the Cloud Computing class at NYU (Taught by Prof. Sambit Sahu).




