from PIL import Image
import sys, os
from gmap_utils import *

def merge_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True):
    
    TYPE, ext = 'r', 'png'
    if satellite:
        TYPE, ext = 's', 'jpg'
    
    x_start, y_start = latlon2xy(zoom, lat_start, lon_start)
    x_stop, y_stop = latlon2xy(zoom, lat_stop, lon_stop)
    
    print "x range", x_start, x_stop
    print "y range", y_start, y_stop
    
    w = (x_stop - x_start) * 256
    h = (y_stop - y_start) * 256
    
    print "width:", w
    print "height:", h
    
    result = Image.new("RGBA", (w, h))
    print "Created!"
    jindu = 0.00
    jindu_all = (x_stop - x_start) * (y_stop - y_start)
    for x in xrange(x_start, x_stop):
        for y in xrange(y_start, y_stop):
            
            filename = "%d_%d_%d_%s.%s" % (zoom, x, y, TYPE, ext)
            filepng = "%d_%d_%d_%s.png" % (zoom, x, y, TYPE)
            
            if not os.path.exists(filename):
                print "-- missing", filename
                continue
                    
            x_paste = (x - x_start) * 256
            y_paste = h - (y_stop - y) * 256
            
            try:
                ii = Image.open(filename)
                ii.save(filepng)
                i = Image.open(filepng)
            except Exception, e:
                print "-- %s, removing %s" % (e, filename)
                trash_dst = os.path.expanduser("~/.Trash/%s" % filename)
                os.rename(filename, trash_dst)
                continue
            jindu += 1
            result.paste(i, (x_paste, y_paste))
            print ((jindu / jindu_all) * 100) , "%"
            del i,ii
            os.remove(filename)
            os.remove(filepng)
    
    result.save("map_%s.png" % (TYPE))

if __name__ == "__main__":
    
    zoom = 20

    lat_start, lon_start = 28.77, 119.88
    lat_stop, lon_stop = 28.63, 120.07
    
    merge_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True)
