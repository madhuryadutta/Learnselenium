import base64
import os
import sys
import random
import time
from imagekitio import ImageKit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

from dotenv import load_dotenv
load_dotenv()

public_key_val = os.environ['PUBLIC_KEY_ENV']
private_key_val = os.environ['PRIVATE_KEY_ENV']
url_endpoint_val = os.environ['URL_ENDPOINT_ENV']

imagekit = ImageKit(
    public_key=public_key_val,
    private_key=private_key_val,
    url_endpoint = url_endpoint_val
)

# get the current time in seconds since the epoch
seconds = time.time()
common_part=str(seconds)[:11]
filename=common_part+'sql'
log_filename=common_part+'.txt'


upload = imagekit.upload(
    file=open("output.sql", "rb"),
    file_name=filename,
    options=UploadFileRequestOptions(
        tags = ["tag1", "tag2"]
    )
)

print("Upload binary", upload)

# Raw Response
print(upload.response_metadata.raw)

# print that uploaded file's ID
print(upload.file_id)

print("*********************************************************************************************************************************8")

upload = imagekit.upload(
    file=open("log.txt", "rb"),
    file_name=log_filename,
    options=UploadFileRequestOptions(
        tags = ["tag1", "tag2"]
    )
)

print("Upload binary", upload)

# Raw Response
print(upload.response_metadata.raw)

# print that uploaded file's ID
print(upload.file_id)
