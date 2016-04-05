from utils import *


####################


def help_pvr_getchannelgroups(self):
    print 'pvr_getchannelgroups: List Channel Groups'
    print 'usage: pvr_getchannelgroups'


def do_pvr_getchannelgroups(self, args):
    gen = self.ph.PVRGetChannelGroups(args)
    for m in gen:
        print m 

def complete_pvr_getchannelgroups(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return tab_completer(['tv','radio'], text)


####################


def help_pvr_getchannelgroupdetails(self):
    print 'pvr_getchannelgroupdetails: Show Details of given Channel Group'
    print 'usage: pvr_getchannelgroupdetails'


def do_pvr_getchannelgroupdetails(self, args):
    (args, _options) = parse_arguments(args)
    group_type = args.pop(0)
    group_name = ' '.join(args)
    gen = self.ph.PVRGetChannelGroupDetails(group_type,group_name)
    for m in gen:
        print "%s. %s" % (m['channelid'],m['label'])

def complete_pvr_getchannelgroupdetails(self, text, line, beg, end):
    all_parts =line.decode('utf-8').split(' ')
    parts = line.split(' ')
    if len(parts) == 2:
        return tab_completer(['tv','radio'], text)

    if len(parts) == 3:
        if parts[1]=='tv':
            return tab_completer(self.ph.PVRGetChannelGroups('tv'), text)
        else:
            return tab_completer(self.ph.PVRGetChannelGroups('radio'), text)

