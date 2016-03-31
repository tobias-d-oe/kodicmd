from utils import *


####################


def help_movie_list(self):
    print 'movies_list: List your movies'
    print 'usage: movies_list'


def do_movie_list(self, args):
    (args, _options) = parse_arguments(args)
    mov = self.ph.LibraryGetMovies()
    for m in mov:
        print m

####################


def help_movie_count(self):
    print 'movie_count: Total of movies'
    print 'usage: movie_count'


def do_movie_count(self, args):
    print len( self.ph.LibraryGetMovies() )


####################

def help_movie_play(self):
    print 'movie_play: Play a movie'
    print 'usage: movie_play Dad Jahr in dem die Welt untergieng'


def do_movie_play(self, args):
    (args, _options) = parse_arguments(args)
    print "Starting Movie:"
    movid = self.ph.Movie2ID(args.pop(0))
    self.ph.PlayerOpen(movid)


def complete_movie_play(self, text, line, beg, end):
    mline = line.partition(' ')[2]
    offs = len(mline) - len(text)
    return [s[offs:] for s in self.ph.LibraryGetMovies() if s.startswith(mline)]

####################

def help_movie_getdetails(self):
    print 'movie_getdetails: Get movie details'
    print 'usage: movie_getdetails Das Jahr in dem die Welt untergieng'


def do_movie_getdetails(self, args):
    (args, _options) = parse_arguments(args)
    #print args.pop(0)
    res = self.ph.MovieDetails(self.ph.Movie2ID(args.pop(0)))
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
    

def complete_movie_getdetails(self, text, line, beg, end):
    mline = line.partition(' ')[2]
    offs = len(mline) - len(text)
    return [s[offs:] for s in self.ph.LibraryGetMovies() if s.startswith(mline)]


####################

def help_movie_setdetail(self):
    print 'movie_setdetail: Set a property of a movie'
    print 'usage: movie_setdetail \'Das Jahr in dem die Welt untergieng\' fanart \'file://Fanarts/myfanart.jpeg\''


def do_movie_setdetail(self, args):
    (args, _options) = parse_arguments(args)
    res = self.ph.MovieSetDetail(args[0],args[1],args[2])
    print res


def complete_movie_setdetail(self, text, line, beg, end):
    parts = line.split(' ')
    if len(parts) == 2:
        return tab_completer(self.ph.LibraryGetMovies(), text)
    if len(parts) == 3:
        return tab_completer(['trailer','top250','runtime','playcount','sorttitle','cast','country','originaltitle','movieid','dateadded','title','rating','tagline','file','setid','plot','votes','fanart','mpaa','streamdetails','writer','thumbnail','resume','director','imdbnumber','studio','genre'], text)


####################


def help_movie_listgenre(self):
    print 'movies_listgenre: List your movie genres'
    print 'usage: movies_listgenre'


def do_movie_listgenre(self, args):
    (args, _options) = parse_arguments(args)
    gen = self.ph.LibraryGetMovieGenre()
    for m in gen:
        print m


