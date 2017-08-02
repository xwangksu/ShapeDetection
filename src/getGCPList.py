'''
Created on Aug 2, 2017

@author: xuwang
'''
import pymysql
import argparse
import csv

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(prog = 'getGCPList')
ap.add_argument("--expid", required=True,
    help="experiment ID to locate the field where GCPs are placed")
ap.add_argument("--output", required=True,
    help="output file of GCPs")
args = vars(ap.parse_args())
exp_id = args["expid"]
outputFile = open(args["output"],'wt')

# Connect to the database
conn = pymysql.connect(host='beocat.cis.ksu.edu', port=6306,
                       user='xuwang', passwd = 'xuwang',
                       db='wheatgenetics')
try:
    writer = csv.writer(outputFile, delimiter=',', lineterminator='\n')
    writer.writerow(('Index','Longitude','Latitude','Altitude'))
    with conn.cursor() as cursor:
        querySQLString = "SELECT gcp.index,gcp.longitude,gcp.latitude,gcp.altitude FROM gcp WHERE gcp.experiment = %s"
        cursor.execute(querySQLString, (exp_id))
        for row in cursor:
            writer.writerow(row)

finally:
    cursor.close()
    conn.close()