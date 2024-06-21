"""
This module provides a CLI tool to convert natural language descriptions into REST API
queries and execute them using the OpenAI's GPT-3.5 Turbo model.
"""

import os
import json
import argparse
import requests
import configparser
from openai import OpenAI

def get_config():
    config = configparser.ConfigParser()
    config_file = 'nlrest.ini'

    if not os.path.exists(config_file):
        config['DEFAULT'] = {'OpenAI_API_Key': 'your-api-key-here', 'Model_Name': 'gpt-3.5-turbo'}
        with open(config_file, 'w') as configfile:
            config.write(configfile)
    else:
        config.read(config_file)

    return config

# Ensure the config is loaded before initializing the OpenAI client
config = get_config()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY", config['DEFAULT'].get('OpenAI_API_Key')))

def get_rest_query_details(prompt, config, client):
    """
    Generates REST API query details from a natural language prompt using OpenAI's GPT-3.5 Turbo model.

    Args:
        prompt (str): The natural language prompt for generating the REST API query.
        config (dict): The configuration object.
        client: The OpenAI client object.

    Returns:
        dict: The details of the REST API query including method, url, headers, body, and params.
    """
    
    system_message = (
        "You are a REST API assistant. Convert natural language instructions "
        "into REST API query details. Respond with a JSON object that includes "
        "'method', 'url', 'headers', 'body', and 'params'. Example: "
        '{"method": "GET", "url": "https://api.example.com/data", '
        '"headers": {"Authorization": "Bearer YOUR_API_KEY"}, '
        '"params": {"query": "value"}, "body": null}.'
    )
    model_name = config['DEFAULT']['Model_Name']
    try:
        response = client.chat.completions.create(model=model_name,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ])
        response_data = json.loads(response.choices[0].message.content)
        validate_response_structure(response_data)
        return response_data
    except Exception as e:
        print(f"Error occurred during API call: {str(e)}")
        return None

def validate_response_structure(response_data):
    """
    Validates the structure of the response from the OpenAI API.

    Args:
        response_data (dict): The response data from the OpenAI API.

    Raises:
        ValueError: If the response data does not contain the expected fields.
    """
    expected_fields = ['method', 'url', 'headers', 'body', 'params']
    for field in expected_fields:
        if field not in response_data:
            raise ValueError(f"Response data is missing the '{field}' field.")

def sanitize_input(input_string):
    """
    Sanitizes the input string to prevent potential security vulnerabilities.

    Args:
        input_string (str): The input string to be sanitized.

    Returns:
        str: The sanitized input string.
    """
    # Add sanitization logic here
    return input_string


def make_request(api_details):
    """
    Makes an HTTP request based on the provided API details.

    Args:
        api_details (dict): The details of the API including method, url, headers, body, and params.

    Returns:
        str: The text response from the API call.
    """
    method = api_details.get("method").lower()
    url = api_details.get("url")
    headers = api_details.get("headers", {})
    params = api_details.get("params", {})
    body = api_details.get("body", {})
    timeout = 10  # Timeout in seconds

    if method in ["get", "delete"]:
        response = requests.request(
            method, url, headers=headers, params=params, timeout=timeout
        )
    elif method in ["post", "put", "patch"]:
        response = requests.request(
            method, url, headers=headers, json=body, timeout=timeout
        )
    else:
        raise ValueError("Unsupported HTTP method")

    return response.text


def main():
    config = get_config()

    parser = argparse.ArgumentParser(
        description="Natural Language to REST API Query Converter"
    )
    parser.add_argument(
        "-p", "--prompt", type=str, required=False, 
        help="Natural language prompt for REST API query"
    )
    parser.add_argument(
        "--set-api-key", type=str, 
        help="Set the OpenAI API key in the configuration file"
    )

    args = parser.parse_args()

    if args.set_api_key:
        config['DEFAULT']['OpenAI_API_Key'] = args.set_api_key
        with open('nlrest.ini', 'w') as configfile:
            config.write(configfile)
        print("OpenAI API key updated in configuration file.")
        return

    if args.prompt:
        api_query_details = get_rest_query_details(args.prompt, config, client)
        result = make_request(api_query_details)
        print(result)
    else:
        print("Please provide a prompt using the -p or --prompt option.")


if __name__ == "__main__":
    main()
