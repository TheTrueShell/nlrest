import os
import json
import argparse
import openai
import requests

def get_rest_query_details(prompt):
    openai.api_key = os.getenv('OPENAI_API_KEY')
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a REST API assistant. Convert natural language instructions into REST API query details. Respond with a JSON object that includes 'method', 'url', 'headers', 'body', and 'params'. Example: {\"method\": \"GET\", \"url\": \"https://api.example.com/data\", \"headers\": {\"Authorization\": \"Bearer YOUR_API_KEY\"}, \"params\": {\"query\": \"value\"}, \"body\": null}."},
            {"role": "user", "content": prompt}
        ]
    )
    return json.loads(response.choices[0].message.content)

def make_request(api_details):
    method = api_details.get('method').lower()
    url = api_details.get('url')
    headers = api_details.get('headers', {})
    params = api_details.get('params', {})
    body = api_details.get('body', {})

    if method in ['get', 'delete']:
        response = requests.request(method, url, headers=headers, params=params)
    elif method in ['post', 'put', 'patch']:
        response = requests.request(method, url, headers=headers, json=body)
    else:
        raise ValueError("Unsupported HTTP method")

    return response.text

def main():
    parser = argparse.ArgumentParser(description="Natural Language to REST API Query Converter")
    parser.add_argument('-p', '--prompt', type=str, required=True, help="Natural language prompt for REST API query")
    
    args = parser.parse_args()
    
    api_query_details = get_rest_query_details(args.prompt)
    result = make_request(api_query_details)
    print(result)

if __name__ == "__main__":
    main()
