'''
Created on Jul 18, 2017

@author: xuwang
'''
from rasterstats import zonal_stats
import csv

dateStamp = "20170609"
canopyShapeFile = "E:/xuwang/2017_ASH_LF_traits/17ASH_LF_"+dateStamp+"/shapefiles/height_2_s60.shp"
demFile = "E:/xuwang/2017_ASH_LF_traits/17ASH_LF_"+dateStamp+"/dem.tif"
canopyHeight = zonal_stats(canopyShapeFile, demFile, stats = ['mean','percentile_95'], geojson_out=True)

soilShapeFile = "E:/xuwang/2017_ASH_LF_traits/17ASH_LF_"+dateStamp+"/shapefiles/soil_shape.shp"
soilHeight = zonal_stats(soilShapeFile, demFile, stats = ['percentile_1'], geojson_out=True)

chtLength = len(canopyHeight)

finalFile = open("E:/xuwang/2017_ASH_LF_traits/17ASH_LF_"+dateStamp+"/heightResult_"+dateStamp+".csv",'wt')

try:
    writer = csv.writer(finalFile, delimiter=',', lineterminator='\n')
    writer.writerow(('Plot_ID','Height_mean','Height_95Pct','Height_1Pct','Abs_Height'))
    for i in range(0,chtLength):
        writer.writerow((canopyHeight[i]['properties'].get('Plot_ID'),
                         canopyHeight[i]['properties'].get('mean'),
                         canopyHeight[i]['properties'].get('percentile_95'),
                         soilHeight[i]['properties'].get('percentile_1'),
                         canopyHeight[i]['properties'].get('percentile_95')-soilHeight[i]['properties'].get('percentile_1'))),
finally:
    finalFile.close()
