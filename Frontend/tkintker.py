import tkinter as tk
import requests

def new_label(input:int,answer:str):
    label_history = tk.Label(root, text=input, font=("Arial", 18), wraplength=500,anchor='e')
    label_history.pack(fill='both', padx=10)
    
    label_output = tk.Label(root, text=answer, font=("Arial", 18),wraplength=500, anchor='w')
    label_output.pack(fill='both', padx=10)


def on_enter_pressed(event):
    global f
    # Get the text from the Text widget
    input = text.get("1.0", tk.END).strip()
    url = f"http://localhost:3000/data/{input}"
    responce = requests.get(url)
    answer = responce.text
    new_label(input,answer)
    text.delete("1.0", tk.END)  # Clear the Text widget after input is processed

input_list=[]
root = tk.Tk()
root.title("AI")
root.geometry("400x300")
# label the top inside the box
label = tk.Label(root, text="Personal Assistant", font=("Arial", 18))
label.pack()

# label the output inside the box
label_output = tk.Label(root, text="", font=("Arial", 18))
label_output.pack()

# label the history inside the box
label_history = tk.Label(root, text="", font=("Arial", 18))
label_history.pack()

# used to type text
text = tk.Text(root, height=6, font=("Ariel", 18))  # specifing same as label except text not acceptable
text.pack(fill='x', padx=10)  # calling the root same as the features of label
# Bind the Enter key to trigger the function
root.bind("<Return>", on_enter_pressed)

root.mainloop()
