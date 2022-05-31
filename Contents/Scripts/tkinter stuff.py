from tkinter import *
from tkinter import ttk
root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()
valid_spawn_states=["normal", "s_key", "button_intro"]
def retrieve_input(self):
    global output
    output = self.get("1.0","end-1c")
    if not output in valid_spawn_states:
        return print("This is not a valid spawn condition!")
    elif output=="quit":
        sys.exit()
    root.destroy()

ttk.Label(frm, text=f"Enter the spawn state you desire.\nCheck console for output.\nChoices are {', '.join(valid_spawn_states)}").grid(column=1, row=0)
(textBox:=Text(root, height=2, width=10)).grid(column=0, row=1)
buttonCommit=Button(root, height=1, width=10, text="Commit", command=lambda: retrieve_input(textBox)).grid(column=2, row=1)
#command=lambda: retrieve_input() >>> just means do this when i press the button
root.mainloop()