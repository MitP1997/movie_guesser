import json
from tmdb3 import *
set_key('573960af652e25f99356d4bf4c14d987')
set_cache('null')
#from tmdb3 import Movie,Person,Studio
mov = ''
dumpingobject={}
dumpingobject["json"] = []
#341030
x = Movie.mostpopular()
print "done"
counter = 0
for i in x:
    print counter
    counter = counter + 1
    try:
        mov =  i
        #JSON WRITING
        jsonobj = {}
        try:
            jsonobj["id"] = str(mov.id)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["title"] = str(mov.title)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["tagline"] = str(mov.tagline)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["overview"] = str(mov.overview)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["runtime"] = str(mov.runtime)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["budget"] = str(mov.budget)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["revenue"] = str(mov.revenue)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["releasedate"] = str(mov.releasedate).split("-")[0]
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["homepage"] = str(mov.homepage)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        # try:
        #     jsonobj["backdrop"] = str(mov.backdrop.geturl(size='original'))
        # except UnicodeEncodeError:
        #     pass
        # except AttributeError:
        #     pass
        # try:
        #     jsonobj["poster"] = str(mov.poster.geturl(size='original'))
        # except UnicodeEncodeError:
        #     pass
        # except AttributeError:
        #     pass
        try:
            jsonobj["popularity"] = str(mov.popularity)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["userrating"] = str(mov.userrating)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["votes"] = str(mov.votes)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["adult"] = str(mov.adult)
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        try:
            jsonobj["genres"] = []
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        for i in range(0,len(mov.genres)):
            try:
                jsonobj["genres"].append(str(mov.genres[i].name))
            except UnicodeEncodeError:
                pass
            except AttributeError:
                pass
        try:
            jsonobj["studios"] = []
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        for i in range(0,len(mov.studios)):
            try:
                jsonobj["studios"].append(str(mov.studios[i].name))
            except UnicodeEncodeError:
                pass
            except AttributeError:
                pass
        try:
            jsonobj["countries"] = []
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        for i in range(0,len(mov.countries)):
            try:
                jsonobj["countries"].append(str(mov.countries[i].name))
            except UnicodeEncodeError:
                pass
            except AttributeError:
                pass
        try:
            jsonobj["languages"] = []
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        for i in range(0,len(mov.languages)):
            try:
                jsonobj["languages"].append(str(mov.languages[i].code))
            except UnicodeEncodeError:
                pass
            except AttributeError:
                pass
        try:
            jsonobj["cast"] = []
        except UnicodeEncodeError:
            pass
        except AttributeError:
            pass
        length = 5 if (len(mov.cast)>5) else len(mov.cast)
        for i in range(0,length):
            obj = {}
            try:
                obj["name"] = str(mov.cast[i].name)
                obj["character"] = str(mov.cast[i].character)
                jsonobj["cast"].append(obj)
            except UnicodeEncodeError:
                obj["name"] = "mov.cast["+str(i)+"].name"
                jsonobj["cast"].append(obj)
        dumpingobject["json"].append(jsonobj)
    except KeyError:
        pass
    except AttributeError:
        pass
    f = open("movie.json","w")
    f.write(''+json.dumps(dumpingobject))
    f.close()
