"""
This module provides a CLI tool to convert natural language descriptions into REST API
queries and execute them using the OpenAI's GPT-3.5 Turbo model.
"""

import os
import json
import argparse
import openai
import requests


def get_rest_query_details(prompt):
    """
    Generates REST API query details from a natural language prompt using OpenAI's GPT-3.5 Turbo model.

    Args:
        prompt (str): The natural language prompt for generating the REST API query.

    Returns:
        dict: The details of the REST API query including method, url, headers, body, and params.
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    system_message = (
        "You are a REST API assistant. Convert natural language instructions "
        "into REST API query details. Respond with a JSON object that includes "
        "'method', 'url', 'headers', 'body', and 'params'. Example: "
        '{"method": "GET", "url": "https://api.example.com/data", '
        '"headers": {"Authorization": "Bearer YOUR_API_KEY"}, '
        '"params": {"query": "value"}, "body": null}.'
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-1106",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt},
        ],
    )
    return json.loads(response.choices[0].message.content)


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
    """
    Main function to run the nlrest CLI tool.
    """
    parser = argparse.ArgumentParser(
        description="Natural Language to REST API Query Converter"
    )
    parser.add_argument(
        "-p",
        "--prompt",
        type=str,
        required=True,
        help="Natural language prompt for REST API query",
    )

    args = parser.parse_args()

    api_query_details = get_rest_query_details(args.prompt)
    result = make_request(api_query_details)
    print(result)


if __name__ == "__main__":
    main()
