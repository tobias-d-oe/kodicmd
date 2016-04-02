import json
import urllib2
import re


class JSONRPC():
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
#        print data 
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
###
        if "content-type" in response.headers and "charset=" in response.headers['content-type']:
            encoding=response.headers['content-type'].split('charset=')[-1]
            content = unicode(response.read(), encoding)
        else:
            content = unicode(response.read(), "utf-8")
###
#        print content
        return content
    

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

    def PlayerGoTo(self,playerid,where):
        if where != "next" and where != "previous":
            res = self.getJsonResponse(self.host, self.port,'Player.GoTo', { 'playerid': int(playerid), 'to': int(where)})
        else:
            res = self.getJsonResponse(self.host, self.port,'Player.GoTo', { 'playerid': int(playerid), 'to': '%s' % (where)})
        return res

    def PlayerMove(self,playerid,where):
        res = self.getJsonResponse(self.host, self.port,'Player.Move', { 'playerid': int(playerid), 'direction': '%s' % (where)})
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

    def PlayerGetProperty(self, playerid, prop):
        p = []
        p.append(prop)
        res = self.getJsonResponse(self.host, self.port,'Player.GetProperties', { 'properties': p, 'playerid': int(playerid)} )
        return res



    def GetVolume(self):
        res = self.getJsonResponse(self.host, self.port,'Application.GetProperties', { 'properties': ['volume'] })
        return res

    def GetName(self):
        res = self.getJsonResponse(self.host, self.port,'Application.GetProperties', { 'properties': ['name'] })
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

    def LibraryGetMovieGenre(self):
        res = self.getJsonResponse(self.host, self.port,'VideoLibrary.GetGenres', { 'type':'movie' })
        json_obj = json.loads(res)
        res = []
        for gen in json_obj['result']['genres']:
            res.append('%s' % (gen['label'].encode('utf-8')))
        return res


    def Movie2ID(self,movie):
        res = self.getJsonResponse(self.host, self.port,'VideoLibrary.GetMovies', { 'sort': { 'order': 'ascending', 'method': 'label', 'ignorearticle': True } }, id='libMovies')
        json_obj = json.loads(res)
        res = ''
        for mov in json_obj['result']['movies']:
            if mov['label'] == movie:
                res=mov['movieid']
        return res


    def MovieSetDetail(self,movie,key,value):
        va=[]
        print "%s - %s - %s" % (movie,key,value)
        movieid = self.Movie2ID(movie)
        va.append(value)
        res = self.getJsonResponse(self.host, self.port,'VideoLibrary.SetMovieDetails', {'movieid' : int(movieid), '%s' % (key): value})
        print "2"
        print res


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

    def SystemGetAPIVersion(self):
        res = self.getJsonResponse(self.host, self.port,'JSONRPC.Version',)
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

    def SystemPing(self):
        res = self.getJsonResponse(self.host, self.port,'JSONRPC.Ping', )
        res = json.loads(res)
        return res['result']

    def GetSystemTime(self):
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': ['System.Time'] })
        return res

    def GetProperty(self,prop):
        proparray = []
        proparray.append(prop) 
        res = self.getJsonResponse(self.host, self.port,'XBMC.GetInfoLabels',{ 'labels': proparray } )
        return res

    def GetAddons(self):
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddons',  )
        res2 = json.loads(res)
        out = []
        for res in res2['result']['addons']:
             out.append(res['addonid'])
        return out

    def GetBrokenAddons(self):
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddons',  )
        res2 = json.loads(res)
        out = []
        out2 = []
        for res in res2['result']['addons']:
             res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (res['addonid']), 'properties':['name','broken'] }  )
             res = json.loads(res)
             if res['result']['addon']['broken'] != False:
                 out.append(res['result']['addon']['addonid'])
        return out

    def GetDisabledAddons(self):
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddons',  )
        res2 = json.loads(res)
        out = []
        out2 = []
        for res in res2['result']['addons']:
             res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (res['addonid']), 'properties':['name','enabled'] }  )
             res = json.loads(res)
             if res['result']['addon']['enabled'] != True:
                 out.append(res['result']['addon']['addonid'])
        return out



    def GetAddonDetail(self,prop):
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (prop), 'properties':['name','version','summary','description','path','author','thumbnail','fanart','dependencies','broken','extrainfo','rating','enabled'] }  )
        return res

    def GetAddonNamebyID(self,addonid):
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (addonid), 'properties':['name'] }  )
        res = json.loads(res)
        res2 = res['result']['addon']['name']
        return res2

    def GetAddonVersionbyID(self,addonid):
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (addonid), 'properties':['version'] }  )
        res = json.loads(res)
        res2 = res['result']['addon']['version']
        return res2

    def GetAddonPropertybyID(self,addonid,prop):
        p=[]
        p.append(prop)
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddonDetails',{ 'addonid': '%s' % (addonid), 'properties': p }  )
        res = json.loads(res)
        res2 = res['result']['addon'][prop]
        return res2

    def ExecuteAddon(self,addonid):
        res = self.getJsonResponse(self.host, self.port,'Addons.ExecuteAddon',{ 'addonid': '%s' % (addonid) }  )
        return res

    def SetEnabled(self,addonid,isenabled):
        res = self.getJsonResponse(self.host, self.port,'Addons.SetAddonEnabled',{ 'addonid': '%s' % (addonid), 'enabled': json.loads(isenabled) }  )
        return res


    def VideoLibraryScan(self,path=""):
        res = self.getJsonResponse(self.host, self.port,'VideoLibrary.Scan',{ 'directory': '%s' % (path) }  )
        return res

    def VideoLibraryExport(self,path="/tmp"):
        res = self.getJsonResponse(self.host, self.port,'VideoLibrary.Export',{ 'options':{"path": '%s' % (path)} }  )
        return res


    def RC(self,rc):
        res = self.getJsonResponse(self.host, self.port,'Input.ExecuteAction',{ 'action': '%s' % (rc) }  )
        return res
   
    def RC_text(self,text):
        res = self.getJsonResponse(self.host, self.port,'Input.SendText',{ 'text': '%s' % (text) }  )
        return res
   
    def ListSources(self,src):
        res = self.getJsonResponse(self.host, self.port,'Files.GetSources',{'media':'%s' % (src)})
        return res

    def GUIActivateWindow(self,winid):
        res = self.getJsonResponse(self.host, self.port,'GUI.ActivateWindow',{'window':'%s' % (winid)})
        return res

    def GUIGetProperty(self,prop):
        p=[]
        p.append(prop)
        res = self.getJsonResponse(self.host, self.port,'GUI.GetProperties',{'properties':p})
        return res

    def GetSettings(self):
        res = self.getJsonResponse(self.host, self.port,'Settings.GetSettings',  )
        res2 = json.loads(res)
        out = []
        for res in res2['result']['settings']:
             out.append(res)
        return out


    def GetSettingsList(self):
        res = self.getJsonResponse(self.host, self.port,'Settings.GetSettings',  )
        res2 = json.loads(res)
        out = []
        for res in res2['result']['settings']:
             out.append(res['id'])
        return out

    def GetSSetting(self,set):
        res = self.getJsonResponse(self.host, self.port,'Settings.GetSettingValue', { 'setting': '%s' % (set) })
        res2 = json.loads(res)
        return res2['result']['value']

    def SetSetting(self,set,val):
        x = "0123456789"
        match = re.search("^\d+$", x)
        try: 
            x = match.group(0)
            is_int = True
        except AttributeError:
            is_int = False

        if val not in ['true','false'] and not is_int:
            res = self.getJsonResponse(self.host, self.port,'Settings.SetSettingValue', { 'setting': '%s' % (set), 'value': '%s' % (val) })
        else:
            if val == "true":
                val = True
            elif val == "false":
                val = False
            elif is_int:
                val = int(val)
            else:
                print "Problem"
            res = self.getJsonResponse(self.host, self.port,'Settings.SetSettingValue', { 'setting': '%s' % (set), 'value': val })
        return res

    def ResetSetting(self,set):
        res = self.getJsonResponse(self.host, self.port,'Settings.ResetSettingValue', { 'setting': '%s' % (set) })
        return res


    def WhatPlays(self,playerid):
        if playerid == 1:
            res = self.getJsonResponse(self.host, self.port,'Player.GetItem', { 'properties': ["title", "album", "artist", "season", "episode", "duration", "showtitle", "tvshowid", "thumbnail", "file", "fanart", "streamdetails"], 'playerid': int(playerid) })
        elif playerid == 0:
            res = self.getJsonResponse(self.host, self.port,'Player.GetItem', { 'properties': ["title", "album", "artist", "duration", "thumbnail", "file", "fanart", "streamdetails"], 'playerid': int(playerid) })
        res2 = json.loads(res)
        return res2['result']['item']


