import json
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo

"""Functions to take care of the config file tkinter menu option"""

entries = {}

def create_survey_config(main: Tk, txt:Text=None):
    global entries
    top = Toplevel(main)
    top.wm_attributes("-topmost", 1)
    entries = {}
    ttk.Label(top, text=
    "Enter the corresponding value for the config name. The current value is already entered into the field."
    " Instructions are in README.md/on the GitHub", justify="center", wraplength=300).grid(row=0, column=0, columnspan=3)
    row = 1
    with open("config.json","r") as f:
        old = json.load(f)
    for name, old_val in old.items():
        entries[name] = StringVar()
        if name in ["blacklist","wait_unit"]:
            entries[name].set(",".join(str(x) for x in old_val))
        else:
            entries[name].set(str(old_val))
        if name == "os":
            ttk.Label(top, text=name.replace("_", " ").upper()).grid(row=row, column=0)
        else:
            ttk.Label(top, text=name.replace("_", " ").title()).grid(row=row, column=0)
        ttk.Entry(top, textvariable=entries[name], width=50).grid(row=row, column=1, columnspan=2)
        row += 1
    ttk.Button(top, text="Submit", command=lambda: submit_survey(top,txt)).grid(row=row, column=0, columnspan=3, sticky="we", padx=2)

def submit_survey(top:Toplevel,txt:Text=None):
    con = {}
    for name,var in entries.items():
        val = var.get().strip()
        if val == "":
            return
        elif name == "blacklist":
            con[name] = val.replace(", ",",").split(",")
        elif name == "wait_unit":
            con[name] = val.replace(", ",",").split(",")[:-1] + [int(val.replace(", ",",").split(",")[-1])]
        elif name in ["cutoff","cutoff_sec","wait"]:
            con[name] = int(val)
        elif name == "limit":
            if val.title() == "None":
                con[name] = None
            else:
                con[name] = val
        else:
            con[name] = val
    with open("config.json","w") as f:
        json.dump(con,f)
    top.destroy()
    showinfo("Notice","Application restart needed to put changes into effect.")
    if txt is not None:
        txt.config(state=NORMAL)
        txt.delete("1.0", END)
        txt.insert(INSERT, "Success: Edited Config", "a")
        txt.tag_add("center", "1.0", "end")
        txt.config(state=DISABLED)
        txt.see("end")