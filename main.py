import re
import tkinter as tk
from tkinter.filedialog import asksaveasfile
from tkinter import filedialog

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
    8: "argument de fonction",
    9: "nom de fonction",
}

MODS = {
    "A": ("yellow", [2],            1),
    "B": ("red",    [1, 2, 4, 2],   4),
    "C": ("red",    [1, 2, 5, 2],   4),
    "D": ("cyan",   [6],            1),
    "E": ("purple", [3, 2],         1),
    "F": ("blue",   [3, 8],         1),
    "H": ("red",    [1, 2],         2),
    "I": ("red",    [1],            1),
    "L": ("purple", [3, 2],         2),
    "R": ("red",    [1, 2],         2),
    "S": ("yellow", [7],            0),
    "T": ("purple", [9, 8, 1],      1),
    "V": ("red",    [1, 7],         2),
    "X": ("purple", [3, 2],         2),     
    "Z": ("purple", [],             0),
    "//": ("white", [],             0),
}

fenetre = tk.Tk()
fenetre.geometry(geometry)
fenetre.title("kea-editor")
fenetre.configure(background="#000000")

def push():
    global chemin
    if chemin == 0:
        return save_file()
    with open(chemin, "w") as fichier:
        fichier.write(ZCODE.get("1.0", tk.END))

def save_file():
    files = [('KEA', '*.kea'), ('All Files', '*.*')]
    fichier = asksaveasfile(filetypes = files, defaultextension = files)
    if fichier is not None:
        fichier.write(ZCODE.get("1.0", tk.END))
        fichier.close()

def open_file():
    global chemin
    chemin = filedialog.askopenfilename()
    fichier = open(chemin, "r")

    if fichier is not None:
        ZCODE.delete("1.0", tk.END)
        ZCODE.insert(tk.END, fichier.read())
        fichier.close()

def get_dimensions():
    return fenetre.winfo_width(), fenetre.winfo_height()

def setup_editor():
    global ZCODE, VARL, BT_LOAD, BT_SAVE, BT_PUSH, chemin
    chemin = 0
    ZCODE = tk.Text(fenetre, bg="#0C0F1D", fg="#FFFFFF", insertbackground="#00ffff",font=("consolas", 12))
    VARL = tk.Label(fenetre, text="", bg="#12172B", fg="#FFFFFF", anchor="nw", font=("consolas", 12))

    BT_SAVE = tk.Button(fenetre, bg="#12172B", fg="#FFFFFF", text="SAVE AS", command=save_file)
    BT_PUSH = tk.Button(fenetre, bg="#12172B", fg="#FFFFFF", text="SAVE", command=push)
    BT_LOAD = tk.Button(fenetre, bg="#12172B", fg="#FFFFFF", text="LOAD", command=open_file)

    place_editor()

def kill_editor():
    ZCODE.destroy()

def place_editor():
    x, y = get_dimensions()


    if x > 600:
        varlx = ((x - 600) // 10 + 100)
        ZCODE.place(x=varlx, y=30, width=x-varlx, height=y-30)
        VARL.place(x=0, y=0, width=varlx, height=y)
    else:
        varlx = 0
        ZCODE.place(x=0, y=30, width=x, height=y-30)
        VARL.place(x=0, y=0, width=0, height=0)

    BT_SAVE.place(x=varlx, y=0, width=100, height=30)
    BT_PUSH.place(x=varlx+100, y=0, width=100, height=30)
    BT_LOAD.place(x=varlx+200, y=0, width=100, height=30)


def get_text():
    return list(ZCODE.get("1.0", tk.END).split("\n")[:-1])

def recup_element(mod, id, arg):
    return [i+1 for i in range(len(MODS[mod][1])) if MODS[mod][1][i] == id]

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

    def de_a(nb_espaces, arg, e):
        try:
            de = nb_espaces + sum(len(arg[i])+1 for i in range(e))
            a = de + len(arg[e])
            return de, a
        except:
            return 0, 0

    var, bcl = {}, {}

    del_tag()

    for i in range(len(text)):
        nt = text[i]
        while "    " in nt:
            nt = nt.replace("    ", "")

        nb_espaces = len(text[i]) - len(nt)
        
        arg = nt.split(" ")
        mod = arg[0]

        # si la ligne est reconnue
        if mod in MODS.keys():
            # on met le tag du mod
            ZCODE.tag_add(mod, f"{i+1}.{nb_espaces}", f"{i+1}.{nb_espaces + 1}")
            # si le nombre d'arguments est pas bon
            if not (MODS[mod][2] < len(arg) <= len(MODS[mod][1]) + 1):
                BGcode = "er1"
            elif mod == "//":
                BGcode = "comment"
            else:
                for e in recup_element(mod, 1, arg):
                    de, a = de_a(nb_espaces, arg, e)
                    ZCODE.tag_add("Evar", f"{i+1}.{de}", f"{i+1}.{a}")
                    if len(arg) > e and arg[e] not in var.keys():
                        var[arg[e]] = 0

                for e in recup_element(mod, 2, arg):
                    de, a = de_a(nb_espaces, arg, e)
                    if len(arg) > e:
                        if arg[e] in var:
                            ZCODE.tag_add("Ivar", f"{i+1}.{de}", f"{i+1}.{a}")
                            var[arg[e]] += 1
                        else:
                            ZCODE.tag_add("IvarNOSET", f"{i+1}.{de}", f"{i+1}.{a}")

                for e in recup_element(mod, 3, arg):
                    de, a = de_a(nb_espaces, arg, e)
                    ZCODE.tag_add("boucle", f"{i+1}.{de}", f"{i+1}.{a}")
                    bcl[arg[e]] = arg[e] in bcl
                
                for e in recup_element(mod, 9, arg):
                    de, a = de_a(nb_espaces, arg, e)
                    ZCODE.tag_add("boucle", f"{i+1}.{de}", f"{i+1}.{a}")

                for e in recup_element(mod, 7, arg):
                    de, a = de_a(nb_espaces, arg, e)
                    if len(arg) > e:
                        if is_int(arg[e]):
                            ZCODE.tag_add("int", f"{i+1}.{de}", f"{i+1}.{a}")
                        else:
                            ZCODE.tag_add("texte", f"{i+1}.{de}", f"{i+1}.{a}")

                for e in recup_element(mod, 8, arg):
                    de, a = de_a(nb_espaces, arg, e)
                    ZCODE.tag_add("arg", f"{i+1}.{de}", f"{i+1}.{a}")

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
            ZCODE.tag_config("boucle", foreground="#FFFF99")                                        # boucle
            ZCODE.tag_config("arg", foreground="#666666")                                           # argument

    return var, bcl



def actu():
    global old_dim
    new_dim = get_dimensions()

    if old_dim != new_dim:
        print("Dimensions changées", new_dim)
        place_editor()
        old_dim = new_dim

    text = get_text()
    for i in range(len(text)):
        text[i] = text[i].replace("\t", "    ")
    if text != get_text():
        pos = ZCODE.index(tk.INSERT).split(".")
        pos = f'{pos[0]}.' + str(int(pos[1]) + 3)
        ZCODE.delete("1.0", tk.END)
        ZCODE.insert("1.0", "\n".join(text))
        ZCODE.mark_set(tk.INSERT, pos)

    var, bcl = add_colors(get_text())
    var = [f"• {v}" + " " * (7 - len(v)) + f"({var[v]})" for v in var.keys()]
    bcl = [(f"✔ {b}" if bcl[b] else f"❌ {b}") + " " * (10 - len(b)) for b in bcl.keys()]
    VARL.configure(text="VARIABLES:    \n"+"\n".join(var)+"\n\nBOUCLES:      \n"+"\n".join(bcl))

    fenetre.after(250, actu)

setup_editor()
actu()

fenetre.mainloop()