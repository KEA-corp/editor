from errno import errorcode
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
    "A": ("yellow", (2)),
    "B": ("red",    (1,2,4,2)),
    "C": ("red",    (1,2,5,2)),
    "D": ("cyan",   (6)),
    "E": ("purple", (3)),
    "F": ("blue",   (8)),
    "H": ("red",    (1,2)),
    "I": ("red",    (1)),
    "L": ("purple", (3,2)),
    "R": ("red",    (1,2)),
    "S": ("yellow", (7)),
    "T": ("purple", (8)),
    "V": ("red",    (1,7)),
    "X": ("purple", (3,1)),
    "Z": ("purple", ()),
    "//": ("white", ()),
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
        arg = text[i].replace("\t", "").strip().split(" ")
        mod = arg[0]
        if mod in MODS.keys():
            ZCODE.tag_add(mod, f"{i+1}.0", f"{i+1}.1")
            if len(MODS[mod][1]) > 0 and len(MODS[mod][1]) + 1 != len(arg):
                BGcode = "er1"
            elif mod == "//":
                BGcode = "comment"
            else:
                BGcode = "no"

            ZCODE.tag_add(BGcode, f"{i+1}.0", f"{i+1}.{len(text[i])}")
            ZCODE.tag_config(mod, foreground=MODS[mod][0])

    ZCODE.tag_config("er1", background="#554400")        # le nombre d'arguments est incorrect
    ZCODE.tag_config("comment", background="#004400")    # commentaire
    ZCODE.tag_config("no", background="#0C0F1D")         # pas d'erreur



    fenetre.after(250, actu)

setup_editor()
actu()

fenetre.mainloop()