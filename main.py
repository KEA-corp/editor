import re
import tkinter as tk

global old_dim, MODS
geometry = "1050x700"
old_dim = iter(geometry.split("x"))

MODS_DOC = {
    1: "variable de sortie",
    2: "variable d'entrée",
    3: "nom de boucle",
    4: "comparateur",
    5: "opérateur",
    6: "mode de debug",
    7: "texte/valleur",
    8: "nom de fonction",

}

MODS = {
    "A": ("yellow", [2]),
    "B": ("red",    [1,2,4,2]),
    "C": ("red",    [1,2,5,2]),
    "D": ("cyan",   [6]),
    "E": ("purple", [3]),
    "F": ("blue",   [8]),
    "H": ("red",    [1,2]),
    "I": ("red",    [1]),
    "L": ("purple", [3,2]),
    "R": ("red",    [1,2]),
    "S": ("yellow", []),
    "T": ("purple", [8]),
    "V": ("red",    [1,7]),
    "X": ("purple", [3,1]),
    "Z": ("purple", []),
    "//": ("white", []),
}

fenetre = tk.Tk()
fenetre.geometry(geometry)
fenetre.title("kea-editor")
fenetre.configure(background="#000000")

def get_dimensions():
    return fenetre.winfo_width(), fenetre.winfo_height()

def setup_editor():
    global ZCODE, VARL
    ZCODE = tk.Text(fenetre, bg="#0C0F1D", fg="#FFFFFF", insertbackground="#00ffff",font=("consolas", 12))
    VARL = tk.Label(fenetre, text="", bg="#12172B", fg="#FFFFFF", font=("consolas", 12))
    place_editor()

def kill_editor():
    ZCODE.destroy()

def place_editor():
    x, y = get_dimensions()
    if x > 600:
        varlx = ((x - 600) // 10 + 100)
        ZCODE.place(x=varlx, y=0, width=x-varlx, height=y)
        VARL.place(x=0, y=0, width=varlx, height=y)
    else:
        ZCODE.place(x=0, y=0, width=x, height=y)
        VARL.place(x=0, y=0, width=0, height=0)

def get_text():
    return [l.replace("\t", "").replace("    ", "") for l in ZCODE.get("1.0", tk.END).split("\n")[:-1]]

def recup_var(arg):
    if arg[0] in MODS.keys():
        for e in MODS[arg[0]][1]:
            if e == 1:
                return arg[MODS[arg[0]][1].index(e)+1]

def add_colors(text):
    var = []
    for i in range(len(text)):
        arg = text[i].split(" ")
        mod = arg[0]

        # si la ligne est reconnue
        if mod in MODS.keys():
            # on met le tag du mod
            ZCODE.tag_add(mod, f"{i+1}.0", f"{i+1}.1")
            # si le nombre d'arguments est pas bon
            if len(MODS[mod][1]) > 0 and len(MODS[mod][1]) + 1 != len(arg):
                BGcode = f"{i}er1"
            # si c'est un commentaire on met le tag de commentaire
            elif mod == "//":
                BGcode = f"{i}comment"
            # si c'est une ligne classique
            else:
                var.append(recup_var(arg))
                BGcode = "no"
                for _ in [f"{i}er1", f"{i}comment"]:
                    ZCODE.tag_delete(_)
            # on met les tags
            if BGcode != "no":
                ZCODE.tag_add(BGcode, f"{i+1}.0", f"{i+1}.{len(text[i])}")
            ZCODE.tag_config(mod, foreground=MODS[mod][0])           # mod
            ZCODE.tag_config(f"{i}er1", background="#554400")        # le nombre d'arguments est incorrect
            ZCODE.tag_config(f"{i}comment", background="#004400")    # commentaire
    return var



def actu():
    global old_dim
    new_dim = get_dimensions()

    if old_dim != new_dim:
        print("Dimensions changées", new_dim)
        place_editor()
        old_dim = new_dim

    var = add_colors(get_text())

    

    fenetre.after(250, actu)

setup_editor()
actu()

fenetre.mainloop()