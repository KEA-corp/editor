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
    "X": ("purple", [3,2]),
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
    VARL.configure(anchor="nw")
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

def recup_element(mod, id):
    return[i+1 for i in range(len(MODS[mod][1])) if MODS[mod][1][i] == id]


def del_tag():
    for t in ["er1", "comment", "Ever", "Ivar", "no"]:
        ZCODE.tag_delete(t)

def is_int(s):
    try:
        int(s.replace(".", ""))
        return True
    except ValueError:
        return False

def add_colors(text): # sourcery no-metrics
    var, bcl = {}, {}

    del_tag()

    for i in range(len(text)):
        arg = text[i].split(" ")
        mod = arg[0]

        # si la ligne est reconnue
        if mod in MODS.keys():
            # on met le tag du mod
            ZCODE.tag_add(mod, f"{i+1}.0", f"{i+1}.1")
            # si le nombre d'arguments est pas bon
            if len(MODS[mod][1]) > 0 and len(MODS[mod][1]) + 1 != len(arg):
                BGcode = "er1"
            elif mod == "//":
                BGcode = "comment"
            else:
                for e in recup_element(mod, 1):
                    de = sum(len(arg[i])+1 for i in range(e))
                    a = de + len(arg[e])
                    ZCODE.tag_add("Evar", f"{i+1}.{de}", f"{i+1}.{a}")
                    if arg[e] not in var.keys():
                        var[arg[e]] = 0

                for e in recup_element(mod, 2):
                    de = sum(len(arg[i])+1 for i in range(e))
                    a = de + len(arg[e])
                    if arg[e] in var:
                        ZCODE.tag_add("Ivar", f"{i+1}.{de}", f"{i+1}.{a}")
                        var[arg[e]] += 1
                    else:
                        ZCODE.tag_add("IvarNOSET", f"{i+1}.{de}", f"{i+1}.{a}")

                for e in recup_element(mod, 3):
                    de = sum(len(arg[i])+1 for i in range(e))
                    a = de + len(arg[e])
                    ZCODE.tag_add("boucle", f"{i+1}.{de}", f"{i+1}.{a}")
                    bcl[arg[e]] = arg[e] in bcl

                for e in recup_element(mod, 7):
                    de = sum(len(arg[i])+1 for i in range(e))
                    a = de + len(arg[e])
                    if is_int(arg[e]):
                        ZCODE.tag_add("int", f"{i+1}.{de}", f"{i+1}.{a}")
                    else:
                        ZCODE.tag_add("texte", f"{i+1}.{de}", f"{i+1}.{a}")

                BGcode = "no"
            if BGcode != "no":
                ZCODE.tag_add(BGcode, f"{i+1}.0", f"{i+1}.{len(text[i])}")

            ZCODE.tag_config(mod, foreground=MODS[mod][0])                                          # mod
            ZCODE.tag_config("Evar", foreground="cyan", font=("consolas", 12, "bold"))              # variable de sortie
            ZCODE.tag_config("Ivar", foreground="cyan")                                             # variable d'entrée
            ZCODE.tag_config("IvarNOSET", foreground="orange")                                      # variable d'entrée non définie
            ZCODE.tag_config("er1", background="#554400")                                           # le nombre d'arguments est incorrect
            ZCODE.tag_config("comment", background="#004400", font=("consolas", 12, "italic"))      # commentaire
            ZCODE.tag_config("int", foreground="#B5CE89")                                           # nombre
            ZCODE.tag_config("texte", font=("consolas", 12, "italic"))                              # texte

    return var, bcl



def actu():
    global old_dim
    new_dim = get_dimensions()

    if old_dim != new_dim:
        print("Dimensions changées", new_dim)
        place_editor()
        old_dim = new_dim

    var, bcl = add_colors(get_text())
    var = [f"• {v}" + " " * (7 - len(v)) + f"({var[v]})" for v in var.keys()]
    bcl = [(f"✔ {b}" if bcl[b] else f"❌ {b}") + " " * (10 - len(b)) for b in bcl.keys()]
    VARL.configure(text="VARIABLES:    \n"+"\n".join(var)+"\n\nBOUCLES:      \n"+"\n".join(bcl))

    fenetre.after(250, actu)

setup_editor()
actu()

fenetre.mainloop()