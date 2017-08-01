'''
Created on Nov 21, 2016

@author: xuwang
'''
import csv

finalFile = open("D:\\Test_AP_py\\markerList.csv",'wt')

try:
    writer = csv.writer(finalFile)
    writer.writerow(('camera_label','marker_px','marker_py','gcp_longitude',
                    'gcp_latitude','gcp_altitude'))
    
finally:
    finalFile.close()
