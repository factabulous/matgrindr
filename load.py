# -*- coding: utf-8 -*-

import mats
import os
import Tkinter as tk
import myNotebook as nb
from config import config

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def plugin_start():
    this.mats = mats.Materials(local_path("mats.json"))
    return "matgrindr"

def plugin_stop():
    pass

def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    nb.Label(frame, text="Select materials you need").grid()
    this.settings = {}
    for mat in this.mats.names():
        this.settings[mat] = tk.IntVar(value=config.getInt("matgrindr." + mat))
        chk = nb.Checkbutton(parent, text=mat, variable=this.settings[mat]).grid()
    return frame

def prefs_changed(cmdr, is_beta):
    for mat in this.settings:
        config.set("matgrindr." + mat, this.settings[mat].getint())

def plugin_app(parent):
    this.status_frame = nb.frame(parent)
    nb.Label(frame, text="Lat").grid(row=0, col = 0, sticky=W)
    this.lat = nb.Label(frame, text="---").grid(row=0, col = 1)
    nb.Label(frame, text="Lon").grid(row=0, col = 2, sticky=W)
    this.lon = nb.Label(frame, text="===").grid(row=0, col = 3)
    nb.Label(frame, text="Heading").grid(row=1, col=0, sticky=W)
    this.heading nb.Label(frame, text="***").grid(row=1, col=1)
    nb.Label(frame, text="Attitude").grid(row=1, col=2, sticky=W)
    this.attitude = nb.label(frame, text="000").grid(row=1, col=3)
    return this.status_frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
    pass
