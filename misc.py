#
# Licensed under the GNU General Public License Version 3
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2013 Aron Parsons <aronparsons@gmail.com>
# Copyright (c) 2011--2015 Red Hat, Inc.
#

# NOTE: the 'self' variable is an instance of KodiShell

# wildcard import
# pylint: disable=W0401,W0614

# unused argument
# pylint: disable=W0613

# invalid function name
# pylint: disable=C0103

import logging
import readline
import shlex
from getpass import getpass
from ConfigParser import NoOptionError
#from spacecmd.utils import *
from utils import *
from time import sleep
import xmlrpclib

# list of system selection options for the help output
HELP_SYSTEM_OPTS = '''<SYSTEMS> can be any of the following:
name
ssm (see 'help ssm')
search:QUERY (see 'help system_search')
group:GROUP
channel:CHANNEL
'''

HELP_TIME_OPTS = '''Dates can be any of the following:
Explicit Dates:
Dates can be expressed as explicit date strings in the YYYYMMDD[HHMM]
format.  The year, month and day are required, while the hours and
minutes are not; the hours and minutes will default to 0000 if no
values are provided.

Deltas:
Dates can be expressed as delta values.  For example, '2h' would
mean 2 hours in the future.  You can also use negative values to
express times in the past (e.g., -7d would be one week ago).

Units:
s -> seconds
m -> minutes
h -> hours
d -> days
'''

SEPARATOR = '\n' + '#' * 30 + '\n'







import json
import urllib2

class PluginHelpers_JSONRPC():
    def __init__(self):
        self.host     = '127.0.0.1'
        self.port     = '80'
        #self.initdone = False

    def getJsonResponse(self, host, port, method, params=None, id=1):
        url = 'http://%s:%s/jsonrpc' %(host, port)
        values ={}
        values['jsonrpc'] = '2.0'
        values['method'] = method
        if params is not None:
            values['params'] = params
        values['id'] = id  
        headers = {'Content-Type':'application/json'}
    
        data = json.dumps(values)
    
        req = urllib2.Request(url, data, headers)
    
        response = urllib2.urlopen(req)
        return response.read()

    def Init(self, host, port):
        self.host = host
        self.port = port
        self.initdone = True    

    def Prepare(self):
        if not self.initdone:
            self.host = "127.0.0.1"
            self.port = "80"

    def PlayMedia(self, media):
        #self.Prepare()
        res = self.getJsonResponse(self.host, self.port,'Player.Open', { 'item':{'file':'%s' % media} })
        return res
        
    def PlaylistClear(self,num):
        res = self.getJsonResponse(self.host, self.port,'Playlist.Clear' , { 'playlistid' : num } )
        return res

    def PlaylistAdd(self,num,file):
        res = self.getJsonResponse(self.host, self.port, 'Playlist.Add' , { 'playlistid' : 0 , 'item' : {'file' : '%s' % file } } )
        return res

    def PlayPlaylist(self, id):
        res = self.getJsonResponse(self.host, self.port,'Player.Open', { 'item':{'playlistid':'%s' % id} })
        return res

    def GetVolume(self):
        res = self.getJsonResponse(self.host, self.port,'Application.GetProperties', { 'properties': ['volume'] })
        return res

    def SystemSetVolume(self,vol):
        res = self.getJsonResponse(self.host, self.port,'Application.SetVolume', { 'volume': int(vol) })
        return res

    def GetActivePlayer(self):
        res = self.getJsonResponse(self.host, self.port,'Player.GetActivePlayers', )
        return res

    def WhatPlays(self,pl):
        res = self.getJsonResponse(self.host, self.port,'Player.GetItem',)
        return res    
   
    def PlayerPlayPause(self,pl):
        res = self.getJsonResponse(self.host, self.port,'Player.PlayPause',{ 'playerid': pl } )

    def LibraryGetMovies(self):
        res = self.getJsonResponse(self.host, self.port,'VideoLibrary.GetMovies', { 'sort': { 'order': 'ascending', 'method': 'label', 'ignorearticle': True } }, id='libMovies')
        json_obj = json.loads(res)
        res = []
        #print len(json_obj['result']['movies'])
        for mov in json_obj['result']['movies']:
            res.append('%s' % (mov['label'].encode('utf-8')))
        return res

    def Movie2ID(self,movie):
        res = self.getJsonResponse(self.host, self.port,'VideoLibrary.GetMovies', { 'sort': { 'order': 'ascending', 'method': 'label', 'ignorearticle': True } }, id='libMovies')
        json_obj = json.loads(res)
        res = ''
        for mov in json_obj['result']['movies']:
            if mov['label'] == movie:
                res=mov['movieid']
        return res

    def PlayerOpen(self,movieid):
        res = self.getJsonResponse(self.host, self.port,'Player.Open', {"item":{"movieid": movieid }})


    def PlayerStop(self,id):
        res = self.getJsonResponse(self.host, self.port,'Player.Stop', {'playerid': id })




    def MovieDetails(self,movieid):
        res = self.getJsonResponse(self.host, self.port,'VideoLibrary.GetMovieDetails', {"movieid":movieid,"properties":["director","genre","plot","rating","runtime","sorttitle","studio","title","trailer","playcount","originaltitle","tagline","imdbnumber","year","set","setid","dateadded","top250","file","thumbnail","resume","streamdetails","country","tag","mpaa","fanart","cast","votes","writer"]}, id='libMovies')
        return res

    def SystemPlatform(self):
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoBooleans',{"booleans":["System.Platform.Linux","System.Platform.Linux.RaspberryPi","System.Platform.Windows","System.Platform.OSX","System.Platform.IOS","System.Platform.Darwin","System.Platform.ATV2","System.Platform.Android"]})
        res = json.loads(res)

        if res['result']['System.Platform.Linux.RaspberryPi']:
            return "RaspberryPi"
        if res['result']['System.Platform.Linux']:
            return "Linux"
        if res['result']['System.Platform.Windows']:
            return "Windows"
        if res['result']['System.Platform.OSX']:
            return "OSX"

        if res['result']['System.Platform.IOS']:
            return "IOS"

        if res['result']['System.Platform.Darwin']:
            return "Darwin"

        if res['result']['System.Platform.ATV2']:
            return "ATV2"

        if res['result']['System.Platform.Android']:
            return "Android"


    def SystemIsMuted(self):
        res = self.getJsonResponse(self.host, self.port,'Application.GetProperties',{'properties':['volume','muted']})
        res = json.loads(res)
        return res['result']['muted']

    def SystemGetVersion(self):
        res = self.getJsonResponse(self.host, self.port,'Application.GetProperties',{"properties":["version"]})
        res = json.loads(res)
        return res['result']['version']

    def SystemGetKernel(self):
        #res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels","params":{"labels":["System.KernelVersion","System.BuildVersion"]}}
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{'labels':['System.KernelVersion']})
        res = json.loads(res)
        return res['result']['System.KernelVersion']

    def SystemGetBuild(self):
        #res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels","params":{"labels":["System.KernelVersion","System.BuildVersion"]}}
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{'labels':['System.BuildVersion']})
        res = json.loads(res)
        return res['result']['System.BuildVersion']

    def SystemMuteToggle(self,val):
        res = self.getJsonResponse(self.host, self.port,'Application.SetMute',{ 'mute': val })
        res = json.loads(res)
        return res['result']['muted']

    def SystemQuit(self):
        res = self.getJsonResponse(self.host, self.port,'Application.Quit', )
        res = json.loads(res)
        return res['result']['muted']

    def GetSystemTime(self):
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        return res

    def GetProperty(self,prop):
        proparray = []
        proparray.append(prop) 
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': proparray } )
        return res


ph = PluginHelpers_JSONRPC()









def help_clear(self):
    print 'clear: clear the screen'
    print 'usage: clear'


def do_clear(self, args):
    os.system('clear')

####################

####################


def help_system_getvolume(self):
    print 'system_getvolume: Display current volume'
    print 'usage: system_getvolume'


def do_system_getvolume(self, args):
    res = ph.GetVolume()
    res2 = json.loads(res)
    print res2['result']['volume']

####################


def help_system_setvolume(self):
    print 'system_setvolume: ChangeDisplay current volume'
    print 'usage: system_setvolume 55'


def do_system_setvolume(self, args):
    (args, _options) = parse_arguments(args)
    pl = args.pop(0)
    res = ph.SystemSetVolume(pl)


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
        ph.host = host
    elif len(args) == 2:
        host = args.pop(0)
        port = args.pop(0)
        ph.host = host
        ph.port = port

    print "Set %s as request target with port %s" % (ph.host,ph.port)




####################


def help_system_getkernel(self):
    print 'system_getkernel: Display Kernel version'
    print 'usage: system_getkernel'


def do_system_getkernel(self, args):
    print ph.SystemGetKernel()
    #res2 = json.loads(res)
    #print res2['result']['volume']


####################


def help_system_gettime(self):
    print 'system_gettime: Display Kodi Time'
    print 'usage: system_gettime'


def do_system_gettime(self, args):
    res = ph.GetSystemTime()
    res2 = json.loads(res)
    print res2['result']['System.Time']



####################


def help_system_getbuild(self):
    print 'system_getbuild: Display kodi build version'
    print 'usage: system_getbuild'


def do_system_getbuild(self, args):
    print ph.SystemGetBuild()
    #res2 = json.loads(res)
    #print res2['result']['volume']





####################

def help_system_getplatform(self):
    print 'system_getplatform: Display system platform'
    print 'usage: system_getplatform'


def do_system_getplatform(self, args):
    print ph.SystemPlatform()
    #res = ph.GetVolume()
    #res2 = json.loads(res)
    #print res2['result']['volume']


####################

def help_system_ismuted(self):
    print 'system_ismuted: Show muted state'
    print 'usage: system_ismuted'


def do_system_ismuted(self, args):
    print ph.SystemIsMuted()

####################

def help_system_getproperty(self):
    print 'system_getproperty: Show value of a INFO Lable'
    print 'usage: system_getproperty'


def do_system_getproperty(self, args):
    (args, _options) = parse_arguments(args)

    pl = args.pop(0)
    val = ph.GetProperty(pl)
    val = json.loads(val)
    print val['result'][pl]


####################

def help_system_mutetoggle(self):
    print 'system_mutetoggle: toggle mute/unmute'
    print 'usage: system_mutetoggle'


def do_system_mutetoggle(self, args):
    if ph.SystemIsMuted():
        ph.SystemMuteToggle(False)
    else:
        ph.SystemMuteToggle(True)

####################

def help_system_quit(self):
    print 'system_quit: exit kodi'
    print 'usage: system_quit'


def do_system_quit(self, args):
    print ph.SystemQuit()


####################

def help_system_getversion(self):
    print 'system_getversion: Show kodi informations'
    print 'usage: system_getversion'


def do_system_getversion(self, args):
    json_res = ph.SystemGetVersion()
    print "Major      : %s" % (json_res['major'])
    print "Minor      : %s" % (json_res['minor'])
    print "Tag        : %s" % (json_res['tag'])
    print "Revision   : %s" % (json_res['revision'])




####################


def help_player_getactiveplayer(self):
    print 'player_getactiveplayer: Display active player'
    print 'usage: player_getactiveplayer'

def do_player_getactiveplayer(self,args):
    res = ph.GetActivePlayer()
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

    res = ph.PlayerPlayPause(plid)
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

    res = ph.PlayerStop(plid)
    print "Stop %s player (%s)" % (pl,plid)

def complete_player_stop(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(['audio','video','picture'], text)


####################


def help_movie_list(self):
    print 'movies_list: List your movies'
    print 'usage: movies_list'


def do_movie_list(self, args):
    (args, _options) = parse_arguments(args)
    print "Movies:"
    print"--------"
    mov = ph.LibraryGetMovies()
    for m in mov:
        print m


####################

def help_movie_play(self):
    print 'movie_play: Play a movie'
    print 'usage: movie_play Dad Jahr in dem die Welt untergieng'


def do_movie_play(self, args):
    (args, _options) = parse_arguments(args)
    print "Starting Movie:"
    movid = ph.Movie2ID(args.pop(0))
    ph.PlayerOpen(movid)


def complete_movie_play(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(ph.LibraryGetMovies(), text)

####################

def help_movie_details(self):
    print 'movie_details: Get movie details'
    print 'usage: movie_details Das Jahr in dem die Welt untergieng'


def do_movie_details(self, args):
    (args, _options) = parse_arguments(args)
    #print args.pop(0)
    res = ph.MovieDetails(ph.Movie2ID(args.pop(0)))
    res = json.loads(res)
    res = res['result']['moviedetails']
    print "Title          : %s" % (res['title'])
    print "Rating         : %s" % (res['rating'])
    print "Tagline        : %s" % (res['tagline'])
    print "File           : %s" % (res['file'])
    print "Year           : %s" % (res['year'])
    print "Setid          : %s" % (res['setid'])
    print "Plot           : %s" % (res['plot'])
    print "Votes          : %s" % (res['votes'])
    print "Fanart         : %s" % (res['fanart'])
    print "MPAA           : %s" % (res['mpaa'])
    print "Streamdetails  : %s" % (res['streamdetails'])
    print "Writer         : %s" % (res['writer'])
    print "Thumbnail      : %s" % (res['thumbnail'])
    print "Resume         : %s" % (res['resume'])
    print "Director       : %s" % (res['director'])
    print "IMDB           : %s" % (res['imdbnumber'])
    print "Studio         : %s" % (res['studio'])
    print "Genre          : %s" % (res['genre'])
    print "Added          : %s" % (res['dateadded'])
    print "MovieID        : %s" % (res['movieid'])
    print "Orginaltitle   : %s" % (res['originaltitle'])
    print "Country        : %s" % (res['country'])
    print "Cast           : %s" % (res['cast'])
    print "Sorttitle      : %s" % (res['sorttitle'])
    print "Playcount      : %s" % (res['playcount'])
    print "Runtime        : %s" % (res['runtime'])
    print "Top250         : %s" % (res['top250'])
    print "Trailer        : %s" % (res['trailer'])
    

def complete_movie_details(self, text, line, beg, end):
    parts = line.split(' ')

    if len(parts) == 2:
        return tab_completer(ph.LibraryGetMovies(), text)

####################











def help_help(self):
    print 'help: Show help for the given command'
    print 'usage: help COMMAND'

####################


def help_history(self):
    print 'history: List your command history'
    print 'usage: history'


def do_history(self, args):
    for i in range(1, readline.get_current_history_length()):
        print '%s  %s' % (str(i).rjust(4), readline.get_history_item(i))

####################


def help_toggle_confirmations(self):
    print 'toggle_confirmations: Toggle confirmation messages on/off'
    print 'usage: toggle_confirmations'


def do_toggle_confirmations(self, args):
    if self.options.yes:
        self.options.yes = False
        print 'Confirmation messages are enabled'
    else:
        self.options.yes = True
        logging.warning('Confirmation messages are DISABLED!')


####################

def help_whoamitalkingto(self):
    print 'whoamitalkingto: Print the name of the server'
    print 'usage: whoamitalkingto'


def do_whoamitalkingto(self, args):
    print "%s:%s" % (ph.host,ph.port)

####################

#
#def tab_complete_errata(self, text):
#    options = self.do_errata_list('', True)
#    options.append('search:')
#
#    return tab_completer(options, text)
#
#
#def tab_complete_systems(self, text):
#    if re.match('group:', text):
#        # prepend 'group' to each item for tab completion
#        groups = ['group:%s' % g for g in self.do_group_list('', True)]
#
#        return tab_completer(groups, text)
#    elif re.match('channel:', text):
#        # prepend 'channel' to each item for tab completion
#        channels = ['channel:%s' % s
#                    for s in self.do_softwarechannel_list('', True)]
#
#        return tab_completer(channels, text)
#    elif re.match('search:', text):
#        # prepend 'search' to each item for tab completion
#        fields = ['search:%s:' % f for f in self.SYSTEM_SEARCH_FIELDS]
#        return tab_completer(fields, text)
#    else:
#        options = self.get_system_names()
#
#        # add our special search options
#        options.extend(['group:', 'channel:', 'search:'])
#
#        return tab_completer(options, text)
#

def remove_last_history_item(self):
    last = readline.get_current_history_length() - 1

    if last >= 0:
        readline.remove_history_item(last)



def user_confirm(self, prompt='Is this ok [y/N]:', nospacer=False,
                 integer=False, ignore_yes=False):

    if self.options.yes and not ignore_yes:
        return True

    if nospacer:
        answer = prompt_user('%s' % prompt)
    else:
        answer = prompt_user('\n%s' % prompt)

    if re.match('y', answer, re.I):
        if integer:
            return 1
        else:
            return True
    else:
        if integer:
            return 0
        else:
            return False


# replace the current line buffer
def replace_line_buffer(self, msg=None):
    # restore the old buffer if we weren't given a new line
    if not msg:
        msg = readline.get_line_buffer()

    # don't print a prompt if there wasn't one to begin with
    if len(readline.get_line_buffer()):
        new_line = '%s%s' % (self.prompt, msg)
    else:
        new_line = '%s' % msg

    # clear the current line
    self.stdout.write('\r'.ljust(len(self.current_line) + 1))
    self.stdout.flush()

    # write the new line
    self.stdout.write('\r%s' % new_line)
    self.stdout.flush()

    # keep track of what is displayed so we can clear it later
    self.current_line = new_line


def load_config_section(self, section):
    config_opts = ['server', 'username', 'password', 'nossl']

    if not self.config_parser.has_section(section):
        logging.debug('Configuration section [%s] does not exist', section)
        return

    logging.debug('Loading configuration section [%s]', section)

    for key in config_opts:
        # don't override command-line options
        if self.options.__dict__[key]:
            # set the config value to the command-line argument
            self.config[key] = self.options.__dict__[key]
        else:
            try:
                self.config[key] = self.config_parser.get(section, key)
            except NoOptionError:
                pass

    # handle the nossl boolean
    if self.config.has_key('nossl') and isinstance(self.config['nossl'], str):
        if re.match('^1|y|true$', self.config['nossl'], re.I):
            self.config['nossl'] = True
        else:
            self.config['nossl'] = False

    # Obfuscate the password with asterisks
    config_debug = self.config.copy()
    if config_debug.has_key('password'):
        config_debug['password'] = "*" * len(config_debug['password'])

    logging.debug('Current Configuration: %s', config_debug)
