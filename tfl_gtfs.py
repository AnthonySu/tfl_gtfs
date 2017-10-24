#!/usr/bin/python
import subprocess
import shutil
import os
import boto
import boto.s3
from boto.s3.connection import Location
from boto.s3.key import Key
import requests.packages.urllib3
import gzip
import json
import datetime
import time
import tarfile
import glob
import shutil
from filechunkio import FileChunkIO
import math

requests.packages.urllib3.disable_warnings()

start = time.time()

time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d_%H')
time_folder = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d')

file_name = "/home/tflgtfs/data/" + str(time_folder)

# Create folder for day if not exists
if os.path.isdir(file_name) == False:
	os.mkdir(file_name)
	print "Created folder for ", time_folder
	message = "New folder created for " + file_name
	print message

# Call the TfL to GTFS process
subprocess.call("/home/tflgtfs/bin/run")

# Compress and tar the output
print "Tarring and gz'ing"

# Call tar command via command line

file_gtfs = (file_name + "/tfl_gtfs_" + time_stamp + ".tar.gz")
subprocess.call(["tar -zcvf "+file_gtfs+" ./gtfs/"],shell=True)

message = "File has been downloaded and is now .tar.gz"
print message

# Send to AWS S3 bucket
conn = boto.connect_s3(host="s3-eu-west-1.amazonaws.com")
print "Connected to S3"
# Bucket name
bucket_name = "tflgtfsdata"

# Look up bucket, to see if exists 
bucket = conn.lookup(bucket_name)

# If it doesn't, create it 
if not bucket:
	print "Bucket doesn't exist, creating bucket: "
	conn.create_bucket(bucket_name, location=Location.EU)
	message = "First time tfl_gtfs S3 setup. Bucket created " + str(bucket_name)
	print message
else:
	message = "Adding data to: " + str(bucket_name)
	print message

# Connect to the bucket itself
print "connecting to bucket"
b = conn.get_bucket(bucket_name)

# Find file size
upload_chunk_size = 52428800
file_size = os.stat(file_gtfs).st_size
print "file_gtfs size: ", file_size

# Setup a multi part upload request
mp = b.initiate_multipart_upload(os.path.basename(file_gtfs))

# Break data up into sections for sending
chunk_count = int(math.ceil(file_size / float(upload_chunk_size)))
upload_success = False

print "Beginning upload"

# Iterate through sections and fire them off
for i in range(chunk_count):
	print "uploading chunk: ", i
	offset = upload_chunk_size * i
	bytes = min(upload_chunk_size, file_size - offset)
	with FileChunkIO(file_gtfs, 'r', offset=offset,bytes=bytes) as fp:
		mp.upload_part_from_file(fp, part_num=i + 1)
		upload_success = True
mp.complete_upload()
	
message = str(file_gtfs) + " has been uploaded succesfully to S3"
print message
print "upload complete"
upload_success = True

print "Upload success" + str(upload_success)

if upload_success == True:
	# Delete data files (those sent to AWS)
	print "Extracting files for deletion"
	# Extract and unzip file
	subprocess.call(["tar -xvzf " + file_gtfs],shell=True)
	# Delete all the files
	for file in glob.glob(file_gtfs[:-7] + "/*"):
		print "removing file: ", file
		os.remove(file)
	message = "Folder deleted: " + file_name
	print message
	
	# Call the clean process
	subprocess.call("/home/tflgtfs/bin/clean")
	print "Files cleaned up."

else:
	message = "upload error detected, Folder not cleaned up"
	print message

end = time.time()
diff = end-start

