import uvicorn
from fastapi import FastAPI
from call_gpt import chat_completion_request
from get_all_functions import get_list_of_functions
from excecute_command import run_command
import tkinter

app = FastAPI()


# http://localhost:300/"data"
@app.get("/data/{user_data}")
def read_user(user_data: str):
    list_of_functions = get_list_of_functions()
    print(list_of_functions)

    output = chat_completion_request(user_request=user_data, functions=list_of_functions)
    print(output)

    run_command(output)

    return output


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
