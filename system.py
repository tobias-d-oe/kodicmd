from utils import *

####################


def help_system_ping(self):
    print 'system_ping: ping JSON-RPC Interface'
    print 'usage: system_ping'


def do_system_ping(self, args):
    res = self.ph.SystemPing()
    print res



####################


def help_system_getname(self):
    print 'system_getname: Display system name'
    print 'usage: system_getname'


def do_system_getname(self, args):
    res = self.ph.GetName()
    res2 = json.loads(res)
    print res2['result']['name']


####################


def help_system_getvolume(self):
    print 'system_getvolume: Display current volume'
    print 'usage: system_getvolume'


def do_system_getvolume(self, args):
    res = self.ph.GetVolume()
    res2 = json.loads(res)
    print res2['result']['volume']

####################


def help_system_setvolume(self):
    print 'system_setvolume: ChangeDisplay current volume'
    print 'usage: system_setvolume 55'


def do_system_setvolume(self, args):
    (args, _options) = parse_arguments(args)
    pl = args.pop(0)
    res = self.ph.SystemSetVolume(pl)


####################


def help_system_connect(self):
    print 'system_connect: Connect to a kodi instance'
    print 'usage: system_connect 192.168.0.55'


def do_system_connect(self, args):
    (args, _options) = parse_arguments(args)
    if len(args) == 0:
        self.help_system_connect()
    elif len(args) == 1:
        host = args.pop(0)
        self.ph.host = host
    elif len(args) == 2:
        host = args.pop(0)
        port = args.pop(0)
        self.ph.host = host
        self.ph.port = port

    print "Set %s as request target with port %s" % (self.ph.host,self.ph.port)




####################


def help_system_getkernel(self):
    print 'system_getkernel: Display Kernel version'
    print 'usage: system_getkernel'


def do_system_getkernel(self, args):
    dummy = self.ph.SystemGetKernel()
    time.sleep(1)
    print self.ph.SystemGetKernel()
    #res2 = json.loads(res)
    #print res2['result']['volume']


####################


def help_system_gettime(self):
    print 'system_gettime: Display Kodi Time'
    print 'usage: system_gettime'


def do_system_gettime(self, args):
    res = self.ph.GetSystemTime()
    res2 = json.loads(res)
    print res2['result']['System.Time']



####################


def help_system_getbuild(self):
    print 'system_getbuild: Display kodi build version'
    print 'usage: system_getbuild'


def do_system_getbuild(self, args):
    print self.ph.SystemGetBuild()
    #res2 = json.loads(res)
    #print res2['result']['volume']





####################

def help_system_getplatform(self):
    print 'system_getplatform: Display system platform'
    print 'usage: system_getplatform'


def do_system_getplatform(self, args):
    print self.ph.SystemPlatform()
    #res = ph.GetVolume()
    #res2 = json.loads(res)
    #print res2['result']['volume']


####################

def help_system_ismuted(self):
    print 'system_ismuted: Show muted state'
    print 'usage: system_ismuted'


def do_system_ismuted(self, args):
    print self.ph.SystemIsMuted()

####################

def help_system_getproperty(self):
    print 'system_getproperty: Show value of a INFO Lable'
    print 'usage: system_getproperty'


def do_system_getproperty(self, args):
    (args, _options) = parse_arguments(args)

    pl = args.pop(0)
    val = self.ph.GetProperty(pl)
    val = json.loads(val)
    print val['result'][pl]


####################

def help_system_mutetoggle(self):
    print 'system_mutetoggle: toggle mute/unmute'
    print 'usage: system_mutetoggle'


def do_system_mutetoggle(self, args):
    if self.ph.SystemIsMuted():
        self.ph.SystemMuteToggle(False)
    else:
        self.ph.SystemMuteToggle(True)

####################

def help_system_quit(self):
    print 'system_quit: exit kodi'
    print 'usage: system_quit'


def do_system_quit(self, args):
    print self.ph.SystemQuit()


####################

def help_system_getversion(self):
    print 'system_getversion: Show kodi informations'
    print 'usage: system_getversion'


def do_system_getversion(self, args):
    json_res = self.ph.SystemGetVersion()
    print "Major      : %s" % (json_res['major'])
    print "Minor      : %s" % (json_res['minor'])
    print "Tag        : %s" % (json_res['tag'])
    print "Revision   : %s" % (json_res['revision'])

####################

def help_system_getapiversion(self):
    print 'system_getapiversion: Show JSON RPC version'
    print 'usage: system_getapiversion'


def do_system_getapiversion(self, args):
    json_res = self.ph.SystemGetAPIVersion()
    print "Major      : %s" % (json_res['major'])
    print "Minor      : %s" % (json_res['minor'])
    print "Patch      : %s" % (json_res['patch'])





####################
