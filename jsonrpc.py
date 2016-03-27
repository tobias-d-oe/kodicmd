import json
import urllib2

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

    def GetAddons(self):
        res = self.getJsonResponse(self.host, self.port,'Addons.GetAddons',  )
        res2 = json.loads(res)
        out = []
        for res in res2['result']['addons']:
             out.append(res['addonid'])
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


