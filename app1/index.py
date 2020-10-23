import requests

def handler(event, context):
    response = requests.get('https://api.github.com/events')
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/json'
        },
        'body': response.json()
    }
