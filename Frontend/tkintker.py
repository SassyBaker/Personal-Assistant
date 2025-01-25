import tkinter as tk
import requests
import json
def on_enter_pressed(event):
    global f
    # Get the text from the Text widget
    input = text.get("1.0", tk.END).strip() 
    f=open("input.txt","a")
    f.writelines(input+"\n")  
    url=f"http://localhost:3000/{input}"
    responce=requests.get(url)
    answer=json.loads(responce.data.decode("utf-8"))
    label_output.config(text=answer,font=("Arial", 14)) #you can update the pre existing label 
    f.close()
    f_1=open("input.txt","r")
    history=f_1.read()
    label_history.config(text=history,font=("Arial", 14)) #you can update the pre existing label 
    f_1.close()
    text.delete("1.0", tk.END)  # Clear the Text widget after input is processed

root = tk.Tk() 
root.title("AI") 
root.geometry("400x300")
# label the top inside the box
label= tk.Label(root, text="Personal Assistant", font=("Arial",18)) 
label.pack() 

# label the output inside the box
label_output= tk.Label(root, text="", font=("Arial",18)) 
label_output.pack()

# label the history inside the box
label_history= tk.Label(root, text="", font=("Arial",18)) 
label_history.pack() 

# used to type text
text=tk.Text(root,height=6,font=("Ariel",18))# specifing same as label except text not acceptable
text.pack()#calling the root same as the features of label
# Bind the Enter key to trigger the function
root.bind("<Return>", on_enter_pressed)

root.mainloop()  
