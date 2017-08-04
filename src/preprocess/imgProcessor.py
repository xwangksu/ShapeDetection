'''
Created on Aug 3, 2017

@author: xuwang
'''
import exifread
import numpy
import csv
import cv2
import os
import utm
from datetime import datetime

class ImageProcessor:
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
    def getLocationExif(self, srcImage):
        # Get EXIF GPS attributes
        exifAttrib = open(srcImage, 'rb')
        tags = exifread.process_file(exifAttrib, details=False)
        longiRef = -1
        latiRef = 1
        for tag in tags.keys():
            if tag == 'GPS GPSLongitudeRef':
                longiRefStr = str(tags[tag])
        #         print("Longitude Ref: %s" % longiRefStr)
            elif tag == 'GPS GPSLatitudeRef':
                latiRefStr = str(tags[tag])
        #         print("Latitude Ref: %s" % latiRefStr)
            elif tag == 'GPS GPSLatitude':
                latitudeStr = str(tags[tag])[1:-1]
        #         print("Latitude: %s" % latitudeStr)
            elif tag == 'GPS GPSLongitude':
                longitudeStr = str(tags[tag])[1:-1]
        #         print("Longitude: %s" % longitudeStr)
            elif tag == 'GPS GPSAltitude':
                if len(str(tags[tag]).split('/')) == 2:
                    altitude = float(str(tags[tag]).split('/')[0]) / float(str(tags[tag]).split('/')[1])
                else:
                    altitude = float(str(tags[tag]).split('/')[0])
        #         print ("Altitude: %.3f" % altitude)
        if latiRefStr == "N":
            latiRef = 1
        else:
            latiRef = -1
        latitudeDeg = float(latitudeStr.split(',')[0])
        latitudeMin = float(latitudeStr.split(',')[1])
        if len(latitudeStr.split(',')[2].split('/')) == 2:
            latitudeSec = float(latitudeStr.split(',')[2].split('/')[0]) / float(latitudeStr.split(',')[2].split('/')[1])
        else:
            latitudeSec = float(latitudeStr.split(',')[2].split('/')[0])
        latitude = latiRef * (latitudeDeg + latitudeMin / 60 + latitudeSec / 3600)
        # print("Latitude: %.7f" % latitude)
        if longiRefStr == "W":
            longiRef = -1
        else:
            longiRef = 1
        longitudeDeg = float(longitudeStr.split(',')[0])
        longitudeMin = float(longitudeStr.split(',')[1])
        if len(longitudeStr.split(',')[2].split('/')) == 2:
            longitudeSec = float(longitudeStr.split(',')[2].split('/')[0]) / float(longitudeStr.split(',')[2].split('/')[1])
        else:
            longitudeSec = float(longitudeStr.split(',')[2].split('/')[0])
        longitude = longiRef * (longitudeDeg + longitudeMin / 60 + longitudeSec / 3600)
        # print("Latitude: %.7f" % longitude)
        return [longitude, latitude, altitude]
    # End of function

