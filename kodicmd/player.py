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
    print 'usage: player_playpause PLAYER'

def do_player_playpause(self,args):
    (args, _options) = parse_arguments(args)
    if len(args)!=1:
        self.help_player_playpause()
        return

    pl = args.pop(0)
    if pl == 'audio':
        plid = 0
    elif pl == 'video':
        plid = 1
    elif pl == 'picture':
        plid = 2

    res = self.ph.PlayerPlayPause(plid)
    print self.result_beautifier(res)

def complete_player_playpause(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)

####################
def help_player_stop(self):
    print 'player_stop: stop the given player'
    print 'usage: player_stop PLAYER'

def do_player_stop(self,args):
    (args, _options) = parse_arguments(args)
    if len(args)!=1:
        self.help_player_stop()
        return

    pl = args.pop(0)
    if pl == 'audio':
        plid = 0
    elif pl == 'video':
        plid = 1
    elif pl == 'picture':
        plid = 2

    res = self.ph.PlayerStop(plid)
    print self.result_beautifier(res)

def complete_player_stop(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)


####################
####################
def help_player_whatplays(self):
    print 'player_whatplays: show current playing item'
    print 'usage: player_whatplays PLAYER'

def do_player_whatplays(self,args):
    (args, _options) = parse_arguments(args)
    if len(args)!=1:
        self.help_player_whatplays()
        return

    pl = args.pop(0)
    if pl == 'audio':
        plid = 0
    elif pl == 'video':
        plid = 1
    elif pl == 'picture':
        plid = 2

    res = self.ph.WhatPlays(plid)

    if plid==0:
        print "Album        : %s" % (res['album'])
        print "Artist       : %s" % (res['artist'])
        print "Fanart       : %s" % (res['fanart'])
        print "Titel        : %s" % (res['title'])
        print "Label        : %s" % (res['label'])
        print "Thumbnail    : %s" % (res['thumbnail'])
        print "File         : %s" % (res['file'])
        print "Duration     : %s" % (res['duration'])
        print "Type         : %s" % (res['type'])
        print "ID           : %s" % (res['id'])
    elif plid==1:
        print "Title        : %s" % (res['title'])
        print "Label        : %s" % (res['label'])
        print "Type         : %s" % (res['type'])
        #print "Season       : %s" % (res['season'])
        #print "Episode      : %s" % (res['episode'])
        #print "Duration     : %s" % (res['duration'])
        #print "Showtitle    : %s" % (res['showtitle'])
        print "ID           : %s" % (res['id'])
        print "Thumbnail    : %s" % (res['thumbnail'])
        #print "File         : %s" % (res['file'])
        print "Fanart       : %s" % (res['fanart'])
        #print "Streamdetails: %s" % (res['streamdetails'])

    
def complete_player_whatplays(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)

####################

####################
def help_player_getproperty(self):
    print 'player_getproperty: stop the given player'
    print 'usage: player_getproperty <playerid> <property>'

def do_player_getproperty(self,args):
    (args, _options) = parse_arguments(args)
    if len(args)!=2:
        self.help_player_getproperty()
        return

    pl = args[0]
    if pl == 'audio':
        plid = 0
    elif pl == 'video':
        plid = 1
    elif pl == 'picture':
        plid = 2

    prop = args[1]

    res = self.ph.PlayerGetProperty(plid,prop)
    res = json.loads(res)
    res = res['result'][prop]

    print res

def complete_player_getproperty(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)
    if len(parts) == 3:
        return tab_completer([
                              'type',
                              'partymode',
                              'speed',
                              'time',
                              'percentage',
                              'totaltime',
                              'playlistid',
                              'position',
                              'repeat',
                              'shuffled',
                              'canseek',
                              'canchangespeed',
                              'canmove',
                              'canzoom',
                              'canrotate',
                              'canshuffle',
                              'canrepeat',
                              'currentaudiostream',
                              'audiostreams',
                              'subtitleenabled',
                              'currentsubtitle',
                              'subtitles',
                              'live'
                            ], text)
                          

####################

####################
def help_player_goto(self):
    print 'player_goto: play next/previous/specific item'
    print 'usage: player_goto <playerid> <where>'

def do_player_goto(self,args):
    (args, _options) = parse_arguments(args)
    if len(args)!=2:
        self.help_player_goto()
        return

    pl = args[0]
    if pl == 'audio':
        plid = 0
    elif pl == 'video':
        plid = 1
    elif pl == 'picture':
        plid = 2
    res = self.ph.PlayerGoTo(plid,args[1])
    print self.result_beautifier(res)

def complete_player_goto(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)

    if len(parts) == 3:
        return tab_completer(['next','previous'], text)

####################
####################
def help_player_move(self):
    print 'player_move: toggle play/pause at given player'
    print 'usage: player_move <playerid>'

def do_player_move(self,args):
    (args, _options) = parse_arguments(args)
    if len(args)!=2:
        self.help_player_move()
        return

    pl = args[0]
    if pl == 'audio':
        plid = 0
    elif pl == 'video':
        plid = 1
    elif pl == 'picture':
        plid = 2

    res = self.ph.PlayerMove(plid,args[1])
    print self.result_beautifier(res)

def complete_player_move(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)

    if len(parts) == 3:
        return tab_completer(['left','right','up', 'down', 'next', 'skip', 'previous'], text)

