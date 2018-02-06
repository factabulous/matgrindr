# -*- coding: utf-8 -*-

import mats
import events
import os
import Tkinter as tk
import myNotebook as nb
from config import config
import sys
import Queue
import watcher
import visited

this = sys.modules[__name__]	# For holding module globals

this.status_queue = Queue.Queue()

this.debug = 1


def dbgFsdCanis():
    journal_entry("Cmdr", True, "164 G. Canis Majoris", None, {'event': 'FSDJump', 'StarSystem': '164 G. Canis Majoris', 'StarPos': [ 484.125 / -31 / -311.03125]}, {})
def dbgFsdSol():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'FSDJump', 'StarSystem': 'Sol', 'StarPos': [ 0, 0, 0]}, {})

def dbgScExit():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'FSDJump'}, {})

def dbgTouchdownIn():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'Touchdown'}, {})

def dbgTouchdownOut():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'Touchdown'}, {})

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def plugin_start():
    this.visited = visited.Visited() 
    this.mats = mats.Materials(local_file("mats.json"), this.visited)
    selected = config.get("matgrindr.selected") or []
    this.events = events.EventEngine(this.mats, selected)
    return "Matgrindr"

def plugin_stop():
    if this.watcher:
        this.watcher.stop()
        this.watcher.join()

def update():
    try:
        while True:
            status = this.status_queue.get_nowait()
            this.lat.set(str(status['Latitude']))
            this.lon.set(str(status['Longitude']))
            this.status_frame.update_idletasks()
    except Queue.Empty:
        pass
    this.status_frame.after(100, update)

def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    nb.Label(frame, text="Select materials you want").grid()
    this.settings = {}
    selected = config.get("matgrindr.selected") or []
    for mat in this.mats.names():
        v = 0
        if mat in selected:
            v = 1
        this.settings[mat] = tk.IntVar()
        this.settings[mat].set(v)
        chk = nb.Checkbutton(frame, text=mat, variable=this.settings[mat]).grid(sticky=tk.W)

    return frame

def prefs_changed(cmdr, is_beta):
    """
    Called when the preferences have changes - updates the changes in
    permanent storage
    """
    res = []
    for mat in this.mats.names():
        if this.settings[mat].get():
            res.append(mat)
    config.set("matgrindr.selected", res)

def plugin_app(parent):
    """
    Returns a frame containing the status fields we want to display to the 
    app in the main window
    """
    this.status_frame = nb.Frame(parent)
  
    this.action = tk.StringVar() 
    nb.Label(this.status_frame, textvariable=this.action).grid(row=0, column = 0, sticky=tk.W)
    nb.Label(this.status_frame, text="Lat").grid(row=1, column = 0, sticky=tk.W)
    this.lat = tk.StringVar()
    nb.Label(this.status_frame, textvariable=this.lat).grid(row=1, column = 1, sticky=tk.W)

    nb.Label(this.status_frame, text="Lon").grid(row=1, column = 2, sticky=tk.W)
    this.lon = tk.StringVar()
    nb.Label(this.status_frame, textvariable=this.lon).grid(row=1, column = 3)

    nb.Label(this.status_frame, text="Heading").grid(row=2, column=0, sticky=tk.W)
    this.heading = tk.StringVar()
    nb.Label(this.status_frame, textvariable=this.heading).grid(row=2, column=1)
    nb.Label(this.status_frame, text="Attitude").grid(row=1, column=2, sticky=tk.W)
    this.attitude = tk.StringVar()
    nb.Label(this.status_frame, textvariable=this.attitude).grid(row=2, column=3)

    if this.debug:
        nb.Button(this.status_frame, text="FSDJump Sol", command=dbgFsdSol).grid(row=3, sticky=tk.W)
        nb.Button(this.status_frame, text="FSDJump 164 G. Canis Majoris", command=dbgFsdCanis).grid(row=3, column =1, sticky=tk.W)
        nb.Button(this.status_frame, text="SC Exit", command=dbgScExit).grid(sticky=tk.W)
        nb.Button(this.status_frame, text="Touchdown In", command=dbgTouchdownIn).grid(row=5, sticky=tk.W)
        nb.Button(this.status_frame, text="Touchdown Out", command=dbgTouchdownOut).grid(row=5,column =1, sticky=tk.W)
      
    this.watcher = watcher.StatusWatcher(local_file("status.json"), this.status_queue)
    this.watcher.daemon = True
    this.watcher.start()
    parent.after(100, update)
    return this.status_frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
    this.events.process(entry, state)

