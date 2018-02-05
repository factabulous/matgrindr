# -*- coding: utf-8 -*-

import mats
import events
import os
import Tkinter as tk
import myNotebook as nb
from config import config
import sys

this = sys.modules[__name__]	# For holding module globals

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def plugin_start():
    this.mats = mats.Materials(local_file("mats.json"))
    return "matgrindr"

def plugin_stop():
    pass

def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    nb.Label(frame, text="Select materials you need").grid()
    this.settings = {}
    selected = config.get("matgrindr.selected") or []
    for mat in this.mats.names():
        v = mat in selected
        settings[mat] = tk.IntVar(v)
        chk = nb.Checkbutton(parent, text=mat, variable=this.settings[mat]).grid()
    return frame

def prefs_changed(cmdr, is_beta):
    res = []
    for mat in this.mats.names():
        if this.settings[mat].getint():
            res.append(mat)
    config.set("matgrindr.selected", res)

def plugin_app(parent):
    this.status_frame = nb.Frame(parent)
    nb.Label(this.status_frame, text="Lat").grid(row=0, column = 0, sticky=tk.W)
    this.lat = nb.Label(this.status_frame, text="---").grid(row=0, column = 1)
    nb.Label(this.status_frame, text="Lon").grid(row=0, column = 2, sticky=tk.W)
    this.lon = nb.Label(this.status_frame, text="===").grid(row=0, column = 3)
    nb.Label(this.status_frame, text="Heading").grid(row=1, column=0, sticky=tk.W)
    this.heading = nb.Label(this.status_frame, text="***").grid(row=1, column=1)
    nb.Label(this.status_frame, text="Attitude").grid(row=1, column=2, sticky=tk.W)
    this.attitude = nb.label(this.status_frame, text="000").grid(row=1, column=3)
    return this.status_frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
    pass
