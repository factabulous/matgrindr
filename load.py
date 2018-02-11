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
import plug
import heading
from sys import platform
from util import GridHelper

this = sys.modules[__name__]	# For holding module globals

this.status_queue = Queue.Queue()

this.debug = 1

window=tk.Tk()
window.withdraw()


def dbgFsdColonia():
    journal_entry("Cmdr", True, "Colonia", None, {'event': 'FSDJump', 'StarSystem': 'Colonia', 'StarPos': [ -9530.5 , -910.28125 , 19808.125]}, {})

def dbgFsdCanis():
    journal_entry("Cmdr", True, "164 G. Canis Majoris", None, {'event': 'FSDJump', 'StarSystem': '164 G. Canis Majoris', 'StarPos': [ 484.125 , -31 , -311.03125]}, {})

def dbgFsdSol():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'FSDJump', 'StarSystem': 'Sol', 'StarPos': [ 0, 0, 0]}, {})

def dbgScExit5ca():
    journal_entry("Cmdr", True, "164 G. Canis Majoris", "5 c a", {'event': 'SupercruiseExit', 'StarSystem': '164 G. Canis Majoris', 'Body': '5 c a', 'BodyType': 'Planet'}, {})
    
def dbgScExit5cd():
    journal_entry("Cmdr", True, "164 G. Canis Majoris", "5 c d", {'event': 'SupercruiseExit', 'StarSystem': '164 G. Canis Majoris', 'Body': '5 c d', 'BodyType': 'Planet'}, {})

def dbgTouchdownIn():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'Touchdown', 'Latitude': -5, 'Longitude': 3}, {'StarSystem': '164 G. Canis Majoris', 'Body': '5 c a'})

def dbgTouchdownOut():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'Touchdown', 'Latitude': 50, 'Longitude': 30}, {'StarSystem': '164 G. Canis Majoris', 'Body': '5 c a'})

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def plugin_start():
    this.visited = visited.Visited( config.get("matgrindr.visited")) 
    this.mats = mats.Materials(local_file("mats.json"), this.visited)
    selected = config.get("matgrindr.selected") or []
    this.events = events.EventEngine(this.mats, selected, this.visited)
    this._IMG_CLIPBOARD = tk.PhotoImage(file = local_file('clipboard.gif'))
    return "Matgrindr"

def plugin_stop():
    window.destroy()

    if this.watcher:
        this.watcher.stop()
        this.watcher.join()

def update():
    try:
        while True:
            status = this.status_queue.get_nowait()
	    if 'Latitude' in status and 'Longitude' in status:
                this.current_lat.set(status['Latitude'])
                this.current_lon.set(status['Longitude'])
                this.current_heading.set(status['Heading'])
                this.current_altitude.set(str(status['Altitude']))
                if this.target:
                    this.target_heading.set( heading.heading(
                        ( this.current_lat.get(), this.current_lon.get()), 
                        ( this.target['lat'], this.target['lon'])))
                    this.target_attitude.set( heading.rate_of_descent(
                        ( this.current_lat.get(), this.current_lon.get()), 
                        ( this.target['lat'], this.target['lon']),
                        height = status['Altitude'], 
                        radius = this.target['radius']))
                        
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

def copy_system_to_clipboard(event):
   if this.target:
       window.clipboard_clear()  # clear clipboard contents
       window.clipboard_append(this.target['system'])

def plugin_app(parent):
    """
    Returns a frame containing the status fields we want to display to the 
    app in the main window
    """
    h = GridHelper()
    this.status_frame = tk.Frame(parent)
 
    # Current Action being recommended 
    this.action = tk.StringVar() 
    tk.Label(this.status_frame, textvariable=this.action).grid(row=h.row(), column = h.col(3), columnspan=3, sticky=tk.W)
    this.clipboard = tk.Label(this.status_frame, anchor=tk.W, image=this._IMG_CLIPBOARD)
    this.clipboard.grid(row=h.row(), column=h.col())
    this.clipboard.bind("<Button-1>", copy_system_to_clipboard)

    h.newrow()

    # Dynamic Current Location
    tk.Label(this.status_frame, text="Current Lat").grid(row=h.row(), column = h.col(), sticky=tk.W)
    this.current_lat = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.current_lat).grid(row=h.row(), column = h.col(), sticky=tk.W)

    tk.Label(this.status_frame, text="Current Lon").grid(row=h.row(), column = h.col(), sticky=tk.W)
    this.current_lon = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.current_lon).grid(row=h.row(), column = h.col())

    h.newrow()
    tk.Label(this.status_frame, text="Target Lat").grid(row=h.row(), column = h.col(), sticky=tk.W)
    this.target_lat = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.target_lat).grid(row=h.row(), column = h.col(), sticky=tk.W)

    tk.Label(this.status_frame, text="Target Lon").grid(row=h.row(), column = h.col(), sticky=tk.W)
    this.target_lon = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.target_lon).grid(row=h.row(), column = h.col())

    h.newrow()
    # Heading
    tk.Label(this.status_frame, text="Current Heading").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.current_heading = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.current_heading).grid(row=h.row(), column=h.col(), sticky = tk.W)
    tk.Label(this.status_frame, text="Altitude").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.current_altitude = tk.StringVar()
    tk.Label(this.status_frame, textvariable=this.current_altitude).grid(row=h.row(), column=h.col(), sticky = tk.W)

    h.newrow()
    # Target Heading
    tk.Label(this.status_frame, text="Target Heading").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.target_heading = tk.StringVar()
    tk.Label(this.status_frame, textvariable=this.target_heading).grid(row=h.row(), column=h.col(), sticky=tk.W)
    tk.Label(this.status_frame, text="Attitude").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.target_attitude = tk.StringVar()
    tk.Label(this.status_frame, textvariable=this.target_attitude).grid(row=h.row(), column=h.col(), sticky=tk.W)
    if this.debug:
        h.newrow()
        tk.Button(this.status_frame, text="FSDJump Sol", command=dbgFsdSol).grid(row=h.row(), column = h.col(), sticky=tk.W)
        tk.Button(this.status_frame, text="FSDJump Colonia", command=dbgFsdColonia).grid(row=h.row(), column = h.col(), sticky=tk.W)
        h.newrow()
        tk.Button(this.status_frame, text="FSDJump 164 G. Canis Majoris", command=dbgFsdCanis).grid(row=h.row(), column =h.col(), sticky=tk.W)
        tk.Button(this.status_frame, text="Touchdown Out", command=dbgTouchdownOut).grid(row=h.row(),column =h.col(), sticky=tk.W)
        h.newrow()
        tk.Button(this.status_frame, text="Touchdown In", command=dbgTouchdownIn).grid(row=h.row(), column =h.col(), sticky=tk.W)

    # TODO : Not the right value for Darwin - right value for testing
    if platform == "darwin":
        status_loc = local_file("status.json")
    else:
        status_loc = os.path.realpath(os.path.join( config.default_journal_dir, "status.json"))
      
    this.watcher = watcher.StatusWatcher(
        status_loc,
        this.status_queue)
    this.watcher.daemon = True
    this.watcher.start()
    parent.after(100, update)
    return this.status_frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
    res = this.events.process(entry, state)
    if res:
        # The res is a tuple of action + target dict
        plug.show_error("Retrieved " + str(len(res)))
        this.action.set(res[0])
        if len(res) > 1:
            this.target = res[1]
            this.target_lat.set( this.target['lat'] )
            this.target_lon.set( this.target['lon'] )
        if this.visited.is_dirty():
            config.set("matgrindr.visited", this.visited.save())

