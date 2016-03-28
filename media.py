from utils import *

####################

def help_media_sourceslist(self):
    print 'media_sourceslist: Scan given folder for new content for videolibrary'
    print 'usage: media_sourceslist video'


def do_media_sourceslist(self, args):
    (args, _options) = parse_arguments(args)
    res = self.ph.ListSources(args[0])
    res2 = json.loads(res)

    for s in res2['result']['sources']:
        print "%s (%s)" % (s['label'],s['file'])
    
    #print res2['result']['sources'][0]


def complete_media_sourceslist(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return tab_completer(['video','music','pictures','files','programs'], text)



####################

def help_media_scanvideosources(self):
    print 'media_scanvideosources: Scan given folder for new content for videolibrary'
    print 'usage: media_scanvideosources /home/osmc/Media/Movies'


def do_media_scanvideosources(self, args):
    (args, _options) = parse_arguments(args)
    res = self.ph.VideoLibraryScan(args[0])
    print res


