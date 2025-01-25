import uvicorn
from fastapi import FastAPI
from call_gpt import query_llm
import tkinter

app = FastAPI()


# http://localhost:300/"data"
@app.get("/data/{user_data}")
def read_user(user_data: str):
    # list_of_functions

    # output = query_llm(user_data)

    return user_data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
