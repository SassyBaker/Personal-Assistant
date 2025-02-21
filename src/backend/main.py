import uvicorn
from fastapi import FastAPI
from call_gpt import call_gpt_endpoint
from get_all_functions import get_list_of_functions
import tkinter

app = FastAPI()


# http://localhost:300/"data"
@app.get("/data/{user_data}")
def read_user(user_data: str):
    list_of_functions = get_list_of_functions()
    print(list_of_functions)

    output = call_gpt_endpoint(list_of_functions, user_data)
    print(output)

    return output


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
