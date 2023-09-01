import requests
import time
import json


stack_exchange_url = 'https://api.stackexchange.com/2.3/questions'
params = {
    'order': 'desc',
    'sort': 'creation',
    'site': 'stackoverflow',
    'filter': 'withbody',
    'pagesize': 100  
}


api_url = 'http://localhost:5000/get_tags' 
model = 'svc'

batch_size = 20
articles_processed = 0

while True:
    try:
        
        if articles_processed % batch_size == 0:
            
            response = requests.get(stack_exchange_url, params=params)
            if response.status_code == 200:
                
                response_json = json.loads(response.text)

                
                items = response_json.get('items', [])

                
                if len(items) == 0:
                    print("No more questions found in the response.")
                    break

        
        for i in range(articles_processed, min(articles_processed + batch_size, len(items))):
            item = items[i]
            title = item.get('title', '')
            body = item.get('body', '')

            
            payload = {
                'title': title,
                'body': body,
                'model': model  
            }

            
            response = requests.post(api_url, json=payload)
            if response.status_code == 200:
                data = response.json()
                predicted_tags = data
                print("Title: ", title)
                print("Predicted Tags:", predicted_tags)
                print()
                articles_processed += 1
            else:
                print("API request failed with status code:", response.status_code)

        
        user_input = input("Processed {} articles. Enter 'continue' to fetch more, or press Enter to exit: ".format(articles_processed))
        if user_input.lower() != 'continue':
            break 

    except Exception as e:
        print("An error occurred:", str(e))

