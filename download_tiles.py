#!/usr/bin/python

import urllib2
import os, sys
from gmap_utils import *

import time
import random

def download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True):

	start_x, start_y = latlon2xy(zoom, lat_start, lon_start)
	stop_x, stop_y = latlon2xy(zoom, lat_stop, lon_stop)

	print "x range", start_x, stop_x
	print "y range", start_y, stop_y

	user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1'
	headers = { 'User-Agent' : user_agent }
	jindu_now = 0.00
	jindu_all = (stop_y - start_y) * (stop_x - start_x)
	for x in xrange(start_x, stop_x):
		for y in xrange(start_y, stop_y):
			url = None
			filename = None

			if satellite:
				server = random.randint(0, 3)
				url = "http://khm%d.google.com/kh/v=183&x=%d&y=%d&z=%d" % (server, x, y, zoom)
				filename = "%d_%d_%d_s.jpg" % (zoom, x, y)
			else:
				url = "http://mt1.google.com/vt/lyrs=h@162000000&hl=en&x=%d&s=&y=%d&z=%d" % (x, y, zoom)
				filename = "%d_%d_%d_r.png" % (zoom, x, y)
			bytes = None
			try:
				req = urllib2.Request(url, data=None, headers=headers)
				response = urllib2.urlopen(req)
				bytes = response.read()
			except Exception, e:
				print "--", filename, "->", e
				sys.exit(1)
			
			if bytes.startswith("<html>"):
				print "-- forbidden", filename
				sys.exit(1)
			#print "-- saving", filename
			
			f = open(filename,'wb')
			f.write(bytes)
			f.close()
			print "%.2f%%" % ((jindu_now / jindu_all) * 100)
			jindu_now += 1
			time.sleep(random.random() / 10)
			if jindu_now % 7200 == 0:
				watime = random.random() + 600
				print "wating for ", watime, " s..."
				time.sleep(watime)

if __name__ == "__main__":

	zoom = 20

	lat_start, lon_start = 28.77, 119.88
	lat_stop, lon_stop = 28.63, 120.07

	download_tiles(zoom, lat_start, lat_stop, lon_start, lon_stop, satellite=True)
