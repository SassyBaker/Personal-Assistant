"""
It interacts with GPT (LLM) using the Open WebUI API.
https://docs.openwebui.com/getting-started/api-endpoints/

The main goal is to convert user input to a function name using a prompt.
"""

import os
from dotenv import load_dotenv
from requests import post
from json import dumps


# Load configuration from the environment.
load_dotenv()

def chat_completion_request(user_request, functions_list):
    """
    Make a POST request to the chat completion endpoint.

    :param user_request: WHat the user asked for. ex. "play a song".
    :param functions_list: A list of functions that can be run.
    :return: The JSON response from the server or None if the request fails.
    """

    # Define the endpoint URL.
    url = "https://gpt.ovcraft.com/api/chat/completions"

    # Define API key.
    api_key = os.getenv('GPT_API_KEY')

    # Preferred Model is qwen2.5-coder:latest
    model_name = "qwen2.5-coder:latest"

    # Prompt for the request.
    prompt = f"""
                You are an AI assistant whose job is to identify which functions
                you should call based on a natural language prompt.
                The functions you can all are: {functions_list}.
                Your response from now on should be only a function name and the arguments
                you think are most appropriate, if any arguments are needed.
                Try to fully qualify the names of any TV shows and songs.
                For example, when you are asked to play 'BoJack' you should return play_tv_show('BoJack Horseman').
                The string for this request is: '{user_request}'
              """

    # Create the headers for the request.
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Define the payload for the POST request.
    payload = {
        "model": model_name,
        "messages": [{ "role": "user", "content": prompt }]
    }

    # Make the POST request.
    response = post(url, headers=headers, data=dumps(payload))

    # Check the response status.
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]  # Parse the JSON response
    else:
        print(f"ERR: Request failed with status code {response.status_code}: {response.text}")
        return None
