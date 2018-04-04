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
import version
from sys import platform
from util import GridHelper, debug, error
from ttkHyperlinkLabel import HyperlinkLabel

this = sys.modules[__name__]	# For holding module globals

this.status_queue = Queue.Queue()
this.display_hud_elements = False
this.target = None

#this.debug = True if platform == 'darwin' else False
this.NO_VALUE = "---" # Used when we don't have a value for a field
this.debug_buttons = False # Set True to display buttons for debugging

window=tk.Tk()
window.withdraw()


def dbgFsdColonia():
    journal_entry("Cmdr", True, "Colonia", None, {'event': 'FSDJump', 'StarSystem': 'Colonia', 'StarPos': [ -9530.5 , -910.28125 , 19808.125]}, {})

def dbgFsdCanis():
    journal_entry("Cmdr", True, "164 G. Canis Majoris", None, {'event': 'FSDJump', 'StarSystem': '164 G. Canis Majoris', 'StarPos': [ 484.125 , -31 , -311.03125]}, {})

def dbgFsdSol():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'FSDJump', 'StarSystem': 'Sol', 'StarPos': [ 0, 0, 0]}, {})

def dbgTouchdownIn():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'Touchdown', 'Latitude': -5, 'Longitude': 3}, {'StarSystem': '164 G. Canis Majoris', 'Body': '164 G. Canis Majoris 5 c a','StarPos': [ 484.125 , -31 , -311.03125]})

def dbgTouchdownOut():
    journal_entry("Cmdr", True, "Sol", None, {'event': 'Touchdown', 'Latitude': 50, 'Longitude': 30}, {'StarSystem': '164 G. Canis Majoris', 'Body': '164 G. Canis Majoris 5 c a','StarPos': [ 484.125 , -31 , -311.03125]})

def local_file(name):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), name)

def plugin_start():
    watcher.MatsLoaderRemote( local_file("mats-cache.json"), this.status_queue).start()
    this.visited = visited.Visited( config.get("matgrindr.visited")) 
    this.mats = mats.Materials(None, this.visited)
    selected = config.get("matgrindr.selected") or []
    this.events = events.EventEngine(this.mats, selected, this.visited)
    this._IMG_CLIPBOARD = tk.PhotoImage(file = local_file('clipboard-2x.gif'))
    this._IMG_SKIP = tk.PhotoImage(file = local_file('circle-x-2x.gif'))
    return "Matgrindr"

def plugin_stop():
    window.destroy()


def dashboard_entry(cmdr, is_beta, entry):
    if 'Latitude' in entry and 'Longitude' in entry:
        if hasattr(this, 'target'):
            if this.display_hud_elements:
                this.current_lat.set(entry['Latitude'])
                this.current_lon.set(entry['Longitude'])
                this.current_heading.set(entry['Heading'])
            info = heading.target_info( 
                ( entry['Latitude'], entry['Longitude']), 
                ( this.target['lat'], this.target['lon']),
                height = entry['Altitude'],
                radius = this.target['radius'])
            this.current_distance.set(info['distance'])
            this.target_heading.set( info['heading'] )
            this.target_attitude.set( info['descent_angle'])

def update():
    try:
        while True:
            status = this.status_queue.get_nowait()
            if 'mats' in status:
                debug("Mats reload requested")
                this.mats.reload(status['mats'])
            if 'error' in status:
                error("Error: " + status['error'])
                        
            this.status_frame.update_idletasks()
    except Queue.Empty:
        pass
    this.status_frame.after(100, update)

def select_all():
    for m in this.settings:
        this.settings[m].set(1)

def select_none():
    for m in this.settings:
        this.settings[m].set(0)

def plugin_prefs(parent, cmdr, is_beta):
    frame = nb.Frame(parent)
    nb.Label(frame, text="Select materials you want").grid(row = 0, column = 0)
    this.settings = {}
    selected = config.get("matgrindr.selected") or []

    c = 0
    debug("Mats: " + str(this.mats.names()))
    for mat in this.mats.names():
        this.settings[mat] = tk.IntVar()
        this.settings[mat].set(1 if mat in selected else 0)
        chk = nb.Checkbutton(frame, text=mat, variable=this.settings[mat]).grid(sticky=tk.W, row = 1 + c // 2, column = c % 2)
        c = c + 1

    c = c + 2
    nb.Button(frame, text="Select All", command=select_all).grid(sticky=tk.W, row=c //2, column = 0)
    nb.Button(frame, text="Select None", command=select_none).grid(sticky=tk.W, row=c //2, column = 1)
    return frame

def prefs_changed(cmdr, is_beta):
    """
    Called when the preferences have changes - updates the changes in
    permanent storage
    """
    debug("Prefs changed")
    res = []
    for mat in this.mats.names():
        if this.settings[mat].get():
            res.append(mat)
    config.set("matgrindr.selected", res)
    this.events.change_requirements(res)

    update_target(this.events.find_location())

def copy_system_to_clipboard(event):
   if this.target:
       window.clipboard_clear()  # clear clipboard contents
       window.clipboard_append(this.target['system'])

def skip_target(event):
    if this.target:
        this.visited.set_visited(this.target)
        update_target(this.events.find_location())

def blank_field(value):
    """
    Blanks a field to indicate 'no value present'
    """
    value.set( this.NO_VALUE )

def blank_data_fields():
    debug("Blanking data fields")
    blank_field(this.target_lat)
    blank_field(this.target_lon)
    if this.display_hud_elements:
        blank_field(this.current_lat)
        blank_field(this.current_lon)
        blank_field(this.current_heading)
    blank_field(this.current_distance)
    blank_field(this.target_heading)
    blank_field(this.target_attitude)

def plugin_app(parent):
    """
    Returns a frame containing the status fields we want to display to the 
    app in the main window
    """
    h = GridHelper()
    this.status_frame = tk.Frame(parent)

    vcheck = version.Version("matgrindr")
    if vcheck.is_new_version():
        HyperlinkLabel(this.status_frame, url="https://github.com/factabulous/matgrindr", text="New matgrindr version available! Click here").grid(row=h.row(), column=h.col(4), columnspan=4)
        h.newrow()

    # Current Action being recommended 
    this.action = tk.StringVar() 
    tk.Label(this.status_frame, textvariable=this.action).grid(row=h.row(), column = h.col(3), columnspan=3, sticky=tk.W)

    # Put the icons in the same grid pos in their own frame
    icon_frame = tk.Frame(this.status_frame);
    icon_frame.grid(row=h.row(), column = h.col())
    this.clipboard = tk.Label(icon_frame, anchor=tk.W, image=this._IMG_CLIPBOARD)
    this.skip = tk.Label(icon_frame, anchor=tk.W, image=this._IMG_SKIP)
    this.clipboard.pack(side=tk.LEFT)
    this.skip.pack(side=tk.LEFT)
    this.clipboard.bind("<Button-1>", copy_system_to_clipboard)
    this.skip.bind("<Button-1>", skip_target)

    h.newrow()
    tk.Label(this.status_frame, text="What").grid(row=h.row(), column = h.col(), sticky=tk.W)
    this.type = tk.StringVar() 
    tk.Label(this.status_frame, textvariable=this.type).grid(row=h.row(), column = h.col(3), columnspan=3, sticky=tk.W)
    h.newrow()

    # Dynamic Current Location
    if this.display_hud_elements:
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
    if this.display_hud_elements:
        tk.Label(this.status_frame, text="Current Heading").grid(row=h.row(), column=h.col(), sticky=tk.W)
        this.current_heading = tk.DoubleVar()
        tk.Label(this.status_frame, textvariable=this.current_heading).grid(row=h.row(), column=h.col(), sticky = tk.W)
    tk.Label(this.status_frame, text="Distance").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.current_distance = tk.DoubleVar()
    tk.Label(this.status_frame, textvariable=this.current_distance).grid(row=h.row(), column=h.col(), sticky = tk.W)

    h.newrow()
    # Target Heading
    tk.Label(this.status_frame, text="Target Heading").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.target_heading = tk.StringVar()
    tk.Label(this.status_frame, textvariable=this.target_heading).grid(row=h.row(), column=h.col(), sticky=tk.W)
    tk.Label(this.status_frame, text="Target Attitude").grid(row=h.row(), column=h.col(), sticky=tk.W)
    this.target_attitude = tk.StringVar()
    tk.Label(this.status_frame, textvariable=this.target_attitude).grid(row=h.row(), column=h.col(), sticky=tk.W)
    blank_data_fields()
    if this.debug_buttons:
        h.newrow()
        tk.Button(this.status_frame, text="FSDJump Sol", command=dbgFsdSol).grid(row=h.row(), column = h.col(), sticky=tk.W)
        tk.Button(this.status_frame, text="FSDJump Colonia", command=dbgFsdColonia).grid(row=h.row(), column = h.col(), sticky=tk.W)
        h.newrow()
        tk.Button(this.status_frame, text="FSDJump 164 G. Canis Majoris", command=dbgFsdCanis).grid(row=h.row(), column =h.col(), sticky=tk.W)
        tk.Button(this.status_frame, text="Touchdown Out", command=dbgTouchdownOut).grid(row=h.row(),column =h.col(), sticky=tk.W)
        h.newrow()
        tk.Button(this.status_frame, text="Touchdown In", command=dbgTouchdownIn).grid(row=h.row(), column =h.col(), sticky=tk.W)

    parent.after(100, update)
    return this.status_frame

def journal_entry(cmdr, is_beta, system, station, entry, state):
    res = this.events.process(entry, state, this.target)
    update_target(res)

def update_target(res):
    """
    Updates gui fields based on info passed back from the Events object
    """
    debug("update_target {}".format(res))
    if res:
        # The res is a tuple of action + target dict
        #plug.show_error("Retrieved " + str(len(res)))
        this.action.set(res[0])
        if len(res) > 1:
            this.target = res[1]
            this.type.set("{} ({})".format(this.target['type'], this.target['id']))
            if len(res) > 2:
                show_latlon = res[2]
                if show_latlon:
                    this.target_lat.set( this.target['lat'] )
                    this.target_lon.set( this.target['lon'] )
                else:
                    blank_data_fields()
        if this.visited.is_dirty():
            config.set("matgrindr.visited", this.visited.save())

