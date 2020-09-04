#!/usr/bin/env python
import sys
import requests
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

image_url = sys.argv[1] #we pass the url as an argument
import ipdb;ipdb.set_trace()
# cred = credentials.Certificate('path/to/certificate.json')
cred = credentials.Certificate('/home/developer/grofer/credentials/zinc-interface-243315-1e90e041f0a6.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'citric-proxy-241616.appspot.com'
    # 'storageBucket': '<mysuperstorage>.appspot.com'
    # .appspot.com/
})
bucket = storage.bucket()

image_data = requests.get(image_url).content
blob = bucket.blob('new_cool_image.jpg')
blob.upload_from_string(
        image_data,
        content_type='image/jpg'
    )
print(blob.public_url)