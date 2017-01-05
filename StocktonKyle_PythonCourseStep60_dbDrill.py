import time
import datetime
import os
import shutil
import sqlite3
import wx

# Define initial source and destination
initSource = os.getcwd() + '\\'
initTarget = os.getcwd() + '\\backup'

# Connect to database and get timestamp from last file check
conn = sqlite3.connect('DataMgmt.db')
c = conn.cursor()
c.execute("SELECT * FROM fileCheckLog ORDER BY ID DESC LIMIT 1")
lastCheck = c.fetchone()
lastCheckMsg = 'Last file check: ' + lastCheck[1]

# Converts given timestamp to more easily readable format
def timestampConvert(timestamp):
    ts = datetime.datetime.fromtimestamp(timestamp)
    timeString = (str(ts.year) + "-" + str(ts.month) + "-" + str(ts.day) +
                  " " + str(ts.hour) + ":" + str(ts.minute) + ":" +
                  str(int(ts.second)))
    return timeString

# Copies qualifying files from defined source to defined destination
def fileTransfer(x):
    # Get full paths for designated directories
    source = os.path.realpath(sourceEntry.GetValue())
    target = os.path.realpath(targetEntry.GetValue())
    # Make a list of files in source folder
    files = os.listdir(source)
    for f in files:
        # Get file metadata
        fstats = os.stat(source + '\\' + f)
        # if creation date since last check, copy to desination
        if fstats[9] > lastCheck[2]:
            shutil.copy2(source + '\\'+ f, target)
            print ("'" + f + "' created since last check; " +
                   "copied to '" + target + "'.")
        # if last modified date since last check, copy to destination
        elif fstats[8] > lastCheck[2]:
            shutil.copy2(source + '\\'+ f, target)
            print ("'" + f + "' modified since last check; " +
                   "copied to '" + target  + "'.")
    # Add latest timestamp to file check log
    now = time.time()
    nowString = timestampConvert(int(now))
    c.execute ("INSERT INTO fileCheckLog VALUES (?,?,?)",
               ((lastCheck[0] + 1), nowString, now))
    conn.commit()
    # Declare completion
    print "All qualifying files have been copied."
    print "New timestamp created for " + nowString + "."

# Displays a directory dialog box and passes selection to sourceEntry widget
def displaySourceDialog(x):
    dialog = wx.DirDialog(None, "Choose a source folder:",
                          sourceEntry.GetValue(), style=wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        sourceEntry.SetValue(dialog.GetPath())

# Displays a directory dialog box and passes selection to targetEntry widget
def displayTargetDialog(x):
    dialog = wx.DirDialog(None, "Choose a target folder:",
                          targetEntry.GetValue(), style=wx.DD_NEW_DIR_BUTTON)
    if dialog.ShowModal() == wx.ID_OK:
        targetEntry.SetValue(dialog.GetPath())

# Define UI
app = wx.App()
window = wx.Frame(None, title = "Transfer", size = (230, 200))
panel = wx.Panel(window)
lastCheckLabel = wx.StaticText(panel, -1, lastCheckMsg, pos = (0,0))
sourceLabel = wx.StaticText(panel, -1, "Specify a source folder:", pos = (0,20))
sourceEntry = wx.TextCtrl(panel, value = initSource, pos = (0, 40), 
                          style = wx.TE_READONLY)
sourceButton = wx.Button(panel, label = "Browse", pos = (120,40))
sourceButton.Bind(wx.EVT_BUTTON, displaySourceDialog)
targetLabel = wx.StaticText(panel, -1, "Specify a target folder:", pos = (0,70))
targetEntry = wx.TextCtrl(panel, value = initTarget, pos = (0, 90), 
                          style = wx.TE_READONLY)
targetButton = wx.Button(panel, label = "Browse", pos = (120, 90))
targetButton.Bind(wx.EVT_BUTTON, displayTargetDialog)
transferButton = wx.Button(panel, label = "Transfer",
                           pos = (60,120))
transferButton.Bind(wx.EVT_BUTTON, fileTransfer)
window.Show(True)
app.MainLoop()
