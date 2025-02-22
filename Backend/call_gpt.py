import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

def chat_completion_request(user_request, functions):
    """
    Make a POST request to the chat completion endpoint.

    :param user_request: WHat the user asked for. ex. "play a song".
    :param functions: A list of functions that can be run.
    :return: The JSON response from the server or None if the request fails.
    """
    # Define the endpoint URL
    url = "https://gpt.ovcraft.com/api/chat/completions"

    # Define api key
    api_key = os.getenv('GPT_API_KEY')

    # Preferred Model is qwen2.5-coder:latest
    model_name = "qwen2.5-coder:latest"

    messages = [{
        "role": "user",
        "content": f"""You are an AI assistant whose job is to identify which functions 
            you should call based on a natural language prompt. 
            The functions you can all are: {functions}. 
            Your response from now on should be only a function name and the arguments 
            you think are most appropriate, if any arguments are needed. 
            Try to fully qualify the names of any TV shows and songs. 
            For example, when you are asked to play 'BoJack' you should return play_tv_show('BoJack Horseman'). 
            The string for this request is: '{user_request}'"""
    }]

    # Create the headers for the request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Define the payload for the POST request
    payload = {
        "model": model_name,
        "messages": messages
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        output = response.json()['choices'][0]["message"]["content"]
        return output
    else:
        print(f"Request failed with status code {response.status_code}")
        print("Response body:")
        print(response.text)
        return None

# Example usage of the function
if __name__ == "__main__":
    model = "qwen2.5-coder:latest"


    result = chat_completion_request("Play Clear My Head", "spotify_play_new_song(song_name), spotify_pause_song(), spotify_resume_song()")
    if result:
        print("Chat Completion Response:")
        print(json.dumps(result, indent=4))