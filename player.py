from utils import *

####################


def help_player_getactiveplayer(self):
    print 'player_getactiveplayer: Display active player'
    print 'usage: player_getactiveplayer'

def do_player_getactiveplayer(self,args):
    res = self.ph.GetActivePlayer()
    res2 = json.loads(res)
    try:
        id = res2['result'][0]['playerid']
        type = res2['result'][0]['type']
        print "Active Player: %s" % (id)
        print "Player Type  : %s" % (type)
    except:
        print "No Player active"




####################
def help_player_playpause(self):
    print 'player_playpause: toggle play/pause at given player'
    print 'usage: player_playpause <playerid>'

def do_player_playpause(self,args):
    (args, _options) = parse_arguments(args)

    pl = args.pop(0)
    if pl == 'audio':
        plid = 0
    elif pl == 'video':
        plid = 1
    elif pl == 'picture':
        plid = 2

    res = self.ph.PlayerPlayPause(plid)
    print "Play/Pause toggled for %s player (%s)" % (pl,plid)

def complete_player_playpause(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)

####################
def help_player_stop(self):
    print 'player_stop: stop the given player'
    print 'usage: player_stop <playerid>'

def do_player_stop(self,args):
    (args, _options) = parse_arguments(args)

    pl = args.pop(0)
    if pl == 'audio':
        plid = 0
    elif pl == 'video':
        plid = 1
    elif pl == 'picture':
        plid = 2

    res = self.ph.PlayerStop(plid)
    print "Stop %s player (%s)" % (pl,plid)

def complete_player_stop(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)


####################

