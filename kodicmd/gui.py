from utils import *
####################

def help_gui_getproperty(self):
    print 'gui_getproperty: shows the guiproperty'
    print 'usage: gui_getproperty fullscreen'


def do_gui_getproperty(self, args):
    (args, _options) = parse_arguments(args)
    res = self.ph.GUIGetProperty(args.pop(0))
    return res

def complete_gui_getproperty(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:


        return tab_completer([
                              "currentwindow",
                              "currentcontrol",
                              "skin",
                              "fullscreen"
                            ], text)
                          


####################

def help_gui_activatewindow(self):
    print 'gui_activatewindow: activates the given window'
    print 'usage: gui_activatewindow home'


def do_gui_activatewindow(self, args):
    (args, _options) = parse_arguments(args)
    res = self.ph.GUIActivateWindow(args.pop(0))
    print self.result_beautifier(res)


def complete_gui_activatewindow(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
       
        return tab_completer([
                              "home",
                              "programs",
                              "pictures",
                              "filemanager",
                              "files",
                              "settings",
                              "music",
                              "video",
                              "videos",
                              "tv",
                              "pvr",
                              "pvrguideinfo",
                              "pvrrecordinginfo",
                              "pvrtimersetting",
                              "pvrgroupmanager",
                              "pvrchannelmanager",
                              "pvrguidesearch",
                              "pvrchannelscan",
                              "pvrupdateprogress",
                              "pvrosdchannels",
                              "pvrosdguide",
                              "pvrosddirector",
                              "pvrosdcutter",
                              "pvrosdteletext",
                              "systeminfo",
                              "testpattern",
                              "screencalibration",
                              "guicalibration",
                              "picturessettings",
                              "programssettings",
                              "weathersettings",
                              "musicsettings",
                              "systemsettings",
                              "videossettings",
                              "networksettings",
                              "servicesettings",
                              "appearancesettings",
                              "pvrsettings",
                              "tvsettings",
                              "scripts",
                              "videofiles",
                              "videolibrary",
                              "videoplaylist",
                              "loginscreen",
                              "profiles",
                              "skinsettings",
                              "addonbrowser",
                              "yesnodialog",
                              "progressdialog",
                              "virtualkeyboard",
                              "volumebar",
                              "submenu",
                              "favourites",
                              "contextmenu",
                              "infodialog",
                              "numericinput",
                              "gamepadinput",
                              "shutdownmenu",
                              "mutebug",
                              "playercontrols",
                              "seekbar",
                              "musicosd",
                              "addonsettings",
                              "visualisationsettings",
                              "visualisationpresetlist",
                              "osdvideosettings",
                              "osdaudiosettings",
                              "videobookmarks",
                              "filebrowser",
                              "networksetup",
                              "mediasource",
                              "profilesettings",
                              "locksettings",
                              "contentsettings",
                              "songinformation",
                              "smartplaylisteditor",
                              "smartplaylistrule",
                              "busydialog",
                              "pictureinfo",
                              "accesspoints",
                              "fullscreeninfo",
                              "karaokeselector",
                              "karaokelargeselector",
                              "sliderdialog",
                              "addoninformation",
                              "musicplaylist",
                              "musicfiles",
                              "musiclibrary",
                              "musicplaylisteditor",
                              "teletext",
                              "selectdialog",
                              "musicinformation",
                              "okdialog",
                              "movieinformation",
                              "textviewer",
                              "fullscreenvideo",
                              "fullscreenlivetv",
                              "visualisation",
                              "slideshow",
                              "filestackingdialog",
                              "karaoke",
                              "weather",
                              "screensaver",
                              "videoosd",
                              "videomenu",
                              "videotimeseek",
                              "musicoverlay",
                              "videooverlay",
                              "startwindow",
                              "startup",
                              "peripherals",
                              "peripheralsettings",
                              "extendedprogressdialog",
                              "mediafilter"
                            ], text)



