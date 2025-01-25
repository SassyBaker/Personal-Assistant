from ollama import Client

server_ip = 'http://localhost:11434'  # GPT API Endpoint
gpt_model = 'qwen2.5-coder:1.5b'  # General GPT "llama3.1"


def call_gpt_endpoint(list_of_functions, user_input):
    prompt = f"""You are an AI assistant whose job is to identify which functions 
                    you should call based on a natural language prompt. 
                    The functions you can all are: {list_of_functions}. 
                    Your response from now on should be only a function name and the arguments 
                    you think are most appropriate, if any arguments are needed. 
                    Try to fully qualify the names of any TV shows and songs. 
                    For example, when you are asked to play 'BoJack' you should return play_tv_show('BoJack Horseman'). 
                    The string for this request is: '{user_input}'"""

    client = Client(host=server_ip)
    response = client.chat(model='qwen2.5-coder:1.5b', messages=[
        {'role': 'user', 'content': prompt}, ])

    return response['message']['content']


if __name__ == "__main__":
    print(call_gpt_endpoint("prompt", "Func 1, 2, 3"))
