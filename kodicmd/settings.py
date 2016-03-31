from utils import *
import json
####################


def help_settings_getsettings(self):
    print 'settings_getsettings: show all settings'
    print 'usage: settings_getsettings'


def do_settings_getsettings(self, args):
    (args, _options) = parse_arguments(args)

    if len(args) == 0:
        res = self.ph.GetSettings()
        for i in res:
            val = ""
            try:
                if i['value'] != "":
                    print "%s = %s" % (i['id'],i['value'])
                else:
                    print "%s = %s" % (i['id'],"not set")
            except:
                print "%s = %s" % (i['id'],"not set")
    else:
        res = self.ph.GetSSetting(args[0])
        print "%s = %s" % (args[0],res)        

                                                     
def complete_settings_getsettings(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return tab_completer(self.ph.GetSettingsList(), text)


####################
####################


def help_settings_setsettings(self):
    print 'settings_setsettings: show all settings'
    print 'usage: settings_setsettings'


def do_settings_setsettings(self, args):
    (args, _options) = parse_arguments(args)
    res = self.ph.SetSetting(args[0],args[1])
    print res


                                                     
def complete_settings_setsettings(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return tab_completer(self.ph.GetSettingsList(), text)


####################


def help_settings_resetsettings(self):
    print 'settings_resetsettings: show all settings'
    print 'usage: settings_resetsettings'


def do_settings_resetsettings(self, args):
    (args, _options) = parse_arguments(args)
    res = self.ph.ResetSetting(args)
    print res

                                                     
def complete_settings_resetsettings(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return tab_completer(self.ph.GetSettingsList(), text)


####################

