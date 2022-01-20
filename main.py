import tkinter as tk
from turtle import color

global old_dim, MODS
geometry = "1050x700"
old_dim = iter(geometry.split("x"))
MODS = {
    "A": "yellow",
    "B": "red",
    "C": "red",
    "D": "blue",
    "E": "purple",
    "F": "green",
    "H": "red",
    "I": "red",
    "L": "purple",
    "R": "red",
    "S": "yellow",
    "T": "purple",
    "V": "red",
    "X": "purple",
    "Z": "purple",
}

fenetre = tk.Tk()
fenetre.geometry(geometry)
fenetre.title("kea-editor")
fenetre.configure(background="#000000")

def get_dimensions():
    return fenetre.winfo_width(), fenetre.winfo_height()

def setup_editor():
    global ZCODE
    ZCODE = tk.Text(fenetre, bg="#0C0F1D", fg="#FFFFFF", insertbackground="#00ffff",font=("consolas", 12))
    place_editor()

def kill_editor():
    ZCODE.destroy()

def place_editor():
    x, y = get_dimensions()
    ZCODE.place(x=0, y=0, width=x, height=y)

def get_text():
    return ZCODE.get("1.0", tk.END).split("\n")[:-1]

def actu():
    global old_dim
    new_dim = get_dimensions()
    if old_dim != new_dim:
        print("Dimensions changées", new_dim)
        place_editor()
        old_dim = new_dim
    text = get_text()
    for i in range(len(text)):
        mod = text[i].replace("\t", "").strip().split(" ")[0]
        if mod in MODS.keys():
            ZCODE.tag_add(mod, f"{i+1}.0", f"{i+1}.1")
            ZCODE.tag_config(mod, foreground=MODS[mod])



    fenetre.after(250, actu)

setup_editor()
actu()

fenetre.mainloop()