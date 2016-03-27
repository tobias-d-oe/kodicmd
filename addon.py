#import json
#from jsonrpc import JSONRPC
# subcommand addon_*
from utils import *


####################

def help_addon_list(self):
    print 'addon_list: Show installed Addons'
    print 'usage: addon_list'


def do_addon_list(self, args):
    res2 = self.ph.GetAddons()
    for res in res2:
        print res

####################

def help_addon_count(self):
    print 'addon_count: Total of Addons'
    print 'usage: addon_count'


def do_addon_count(self, args):
    res = self.ph.GetAddons()
    print len(res)

####################

def help_addon_detail(self):
    print 'addon_detail: Show detailed information for a movie'
    print 'usage: addon_detail Das Jahr in dem die Welt untergieng'


def do_addon_detail(self, args):
    (args, _options) = parse_arguments(args)
    res=self.ph.GetAddonDetail(args.pop(0))
    res2=json.loads(res)
    daddon=res2['result']['addon'] 
    print "Addonname        : %s" % (daddon['name'])
    print "Version          : %s" % (daddon['version'])
    print "ID               : %s" % (daddon['addonid'])
    print "Author           : %s" % (daddon['author'])
    print "Broken           : %s" % (daddon['broken'])
    print "Dependencies     : %s" % (daddon['dependencies'])
    print "Description      : %s" % (daddon['description'])
    print "Summary          : %s" % (daddon['summary'])
    print "Rating           : %s" % (daddon['rating'])
    print "Path             : %s" % (daddon['path'])
    print "Disclaimer       : %s" % (daddon['disclaimer'])
    print "Extrainfo        : %s" % (daddon['extrainfo'])
    print "Enabled          : %s" % (daddon['enabled'])
    print "Thumbnail        : %s" % (daddon['thumbnail'])
    print "Fanart           : %s" % (daddon['fanart'])

def complete_addon_detail(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(self.ph.GetAddons(), text)

####################

def help_addon_getnamebyid(self,addonid):
    print 'addon_getnamebyid: Total of Addons'
    print 'usage: addon_getnamebyid'


def do_addon_getnamebyid(self, args):
    res = self.ph.GetAddonNamebyID(args)
    print res

def complete_addon_getnamebyid(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(self.ph.GetAddons(), text)

####################

def help_addon_getpropertybyid(self,addonid,property):
    print 'addon_getpropertybyid: Total of Addons'
    print 'usage: addon_getpropertybyid'


def do_addon_getpropertybyid(self, args):
    (args, _options) = parse_arguments(args)

    res = self.ph.GetAddonPropertybyID(args.pop(0),args.pop(0))
    print res

def complete_addon_getpropertybyid(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(self.ph.GetAddons(), text)
    if len(parts) > 2:
        return tab_completer(['name','version','summary','description', 'path', 'author', 'thumbnail', 'disclaimer', 'fanart', 'dependencies', 'broken', 'extrainfo', 'rating', 'enabled'], text)

####################

def help_addon_execute(self,addonid):
    print 'addon_execute: Start an Addon'
    print 'usage: addon_execute'


def do_addon_execute(self, args):
    res = self.ph.ExecuteAddon(args)
    print "done"

def complete_addon_execute(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(self.ph.GetAddons(), text)

####################

def help_addon_enabled(self,addonid):
    print 'addon_enabled: Set Addon enabled/disabled'
    print 'usage: addon_enabled'


def do_addon_enabled(self, args):
    (args, _options) = parse_arguments(args)

    res = self.ph.SetEnabled(args[0],args[1])
    print res

def complete_addon_enabled(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(self.ph.GetAddons(), text)
    if len(parts) > 2:
        return tab_completer(['true','false'], text)

