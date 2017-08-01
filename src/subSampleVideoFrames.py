
import exifread
import numpy
import os
import shutil
import utm

# Function: get EXIF attributes 
def getUTMFromImage(srcImage):
    # Get EXIF GPS attributes
    exifAttrib = open(srcImage, 'rb')
    tags = exifread.process_file(exifAttrib, details=False)
    longiRef = -1
    latiRef = 1
    for tag in tags.keys():
        if tag == 'GPS GPSLongitudeRef':
            longiRefStr = str(tags[tag])
#             print("Longitude Ref: %s" % longiRefStr)
        elif tag == 'GPS GPSLatitudeRef':
            latiRefStr = str(tags[tag])
#             print("Latitude Ref: %s" % latiRefStr)
        elif tag == 'GPS GPSLatitude':
            latitudeStr = str(tags[tag])[1:-1]
    #         print("Latitude: %s" % latitudeStr)
        elif tag == 'GPS GPSLongitude':
            longitudeStr = str(tags[tag])[1:-1]
    #         print("Longitude: %s" % longitudeStr)
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
    [utmX, utmY, latZone, longZone] = utm.from_latlon(latitude, longitude)
    return [utmX, utmY, latZone, longZone]
# End of function

# Set working path
# Set source images path
srcImagePath = "I:/DJI_A01733_C001_20160526_jpeg/"
imageFiles = os.listdir(srcImagePath)
targetImagePath = "I:/DJI_X5R_sub/"

intDisFrames = 2.0

imf = imageFiles[0]
print(srcImagePath+imf)
[x0,y0,latz0,longz0] = getUTMFromImage(srcImagePath+imf)
pointStart = numpy.array((x0,y0))
i=0
for imf in imageFiles:
    [x,y,latz,longz] = getUTMFromImage(srcImagePath+imf)
    pointCurrent = numpy.array((x,y))
    currentInt = numpy.sqrt(numpy.sum((pointCurrent - pointStart) ** 2))
    if currentInt >= intDisFrames:
        pointStart = pointCurrent
        i=i+1
        print("Interval: %.2f, Image: %s, %d" % (currentInt, imf, i))
        shutil.copy2(srcImagePath+imf,targetImagePath+imf)
