#!/usr/bin/python

from pymongo import MongoClient, DESCENDING, ASCENDING
import urllib
import sys
import datetime
import struct

if (len(sys.argv) != 3):
  print ("Usage: getnxpriotdata.py startdate enddate")
  print ("Dateformat:  yyyymmddhhmm in UTC")
  sys.exit(-1)

(start,end) = sys.argv[1:]

if ( (len(start) != 12) or (len(end) != 12)):
  print ("Usage: getnxpriotdata.py startdate enddate")
  print ("Dateformat:  yyyymmddhhmm in UTC")
  sys.exit(-1)

StartDate = datetime.datetime(int(start[0:4]),int(start[4:6]),int(start[6:8]),int(start[8:10]),int(start[10:12]))
EndDate = datetime.datetime(int(end[0:4]),int(end[4:6]),int(end[6:8]),int(end[8:10]),int(end[10:12]))
#sys.stdout.write("From: ")
#print(StartDate)
#sys.stdout.write("  To: ")
#print(EndDate)

# change to YOUR mongodb password 
password = urllib.quote_plus('password')
# change to YOUR mongodb user - here it is the 'mqtt'
client = MongoClient('mongodb://mqtt:' + password + '@127.0.0.1/data')
db = client.data
# the mqtt topic and mongodb collection are all 'nxpriot'
coll = db.nxpriot
cur = coll.find({'when':{'$gt':StartDate,'$lt':EndDate}},sort=[('when', ASCENDING)])  # ,limit=num)
print "timestamp,latitude,longitude,temperature,humidity,pressure,light,airtvoc,airco2"
for e in cur:
   tstamp = e['when'].strftime("%Y%m%dT%H%M%S")
   dat = e['value']
   lat = struct.unpack('<f',dat[0:4])[0]
   long = struct.unpack('<f',dat[4:8])[0]
   temp = struct.unpack('<f',dat[8:12])[0]
   hum = struct.unpack('<f',dat[12:16])[0]
   airtvoc = struct.unpack('<I',dat[16:20])[0]
   airco2 = struct.unpack('<I',dat[20:24])[0]
   pressure = struct.unpack('<I',dat[24:28])[0]
   light = struct.unpack('<I',dat[28:32])[0]
   #print tstamp,lat,long
   print tstamp+","+str(lat)+","+str(long)+","+str(temp)+","+str(hum)+","+str(airtvoc)+","+str(airco2)+","+str(pressure)+","+str(light)


